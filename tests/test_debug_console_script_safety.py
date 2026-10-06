"""
Non-régression - script inline du panneau de debug (debug_utils.py)
--------------------------------------------------------------------
Contexte : render_debug_console_page() et _broadcast_diff() passent
du JS par st.html(unsafe_allow_javascript=True). Ce JS n'est PAS
inséré tel quel : Streamlit le fait d'abord sanitizer côté navigateur
par DOMPurify, qui ne traite PAS le contenu d'un <script> comme du
texte brut (contrairement au parseur HTML standard) — un '<' littéral
n'IMPORTE OÙ dedans (code, string JS, commentaire, ou valeur JSON
interpolée depuis session_state) est lu comme une balise et peut
faire sauter TOUT le script, silencieusement (aucune erreur JS, juste
un onglet de debug qui reste muet). C'est ce qui s'est produit en
vrai : le panneau pop-out restait bloqué sur "En attente de l'onglet
principal…" sans jamais afficher de log.

Deux garde-fous ci-dessous, pour les deux façons dont un '<' peut
revenir :
1. Un futur edit du template écrit un tag HTML littéral (ou un
   commentaire le mentionnant) directement dans le <script> — capté
   par le scan STATIQUE du fichier source.
2. Une valeur de session_state, une fois json.dumps'ée et interpolée
   dans le script, contient un '<' (chaîne HTML-ish stockée en state,
   ou simplement le repr() par défaut d'un objet Python sans
   __repr__, qui contient nativement '<' et '>') — capté par le test
   DYNAMIQUE qui appelle les fonctions avec des valeurs adverses.

Pas de navigateur ici (cf. test_data_testid_smoke.py pour la même
philosophie) : on vérifie l'invariant qui a causé le bug — aucun
chevron dans le texte final d'un <script> — pas le rendu réel.
"""

import ast
import json
import re
from pathlib import Path

import pytest

import debug_utils

DEBUG_UTILS_SRC = Path(__file__).parent.parent / "debug_utils.py"

_SCRIPT_BLOCK_RE = re.compile(r"<script>(.*?)</script>", re.DOTALL)


def _script_blocks(html_body: str) -> list[str]:
    return _SCRIPT_BLOCK_RE.findall(html_body)


def _html_call_template_texts(source: str) -> list[str]:
    """Reconstruit, pour chaque appel st.html(...) du fichier source,
    le texte de son premier argument — en ne gardant QUE les morceaux
    littéraux d'une f-string et en remplaçant chaque {expression}
    interpolée par un placeholder neutre.

    Un scan naïf "<script>...</script>" sur le fichier ENTIER se fait
    piéger par toute prose (docstring, commentaire) qui mentionne
    "<script>" pour EXPLIQUER ce bug ailleurs dans le fichier — ça
    matche depuis cette mention jusqu'au premier "</script>" réel,
    bien plus loin, capturant du code Python au passage. Passer par
    l'AST cible précisément ce qui part réellement vers le navigateur.
    """
    tree = ast.parse(source)
    templates = []
    for node in ast.walk(tree):
        is_html_call = (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "html"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "st"
            and node.args
        )
        if not is_html_call:
            continue
        arg = node.args[0]
        if isinstance(arg, ast.JoinedStr):
            parts = [
                v.value if isinstance(v, ast.Constant) else "PLACEHOLDER"
                for v in arg.values
            ]
            templates.append("".join(parts))
        elif isinstance(arg, ast.Constant):
            templates.append(arg.value)
    return templates


def _assert_no_stray_chevron(blocks: list[str], *, source_label: str):
    assert blocks, f"aucun bloc <script> trouvé dans {source_label} — le test ne vérifie plus rien"
    for block in blocks:
        assert "<" not in block, (
            f"'<' littéral trouvé dans un <script> de {source_label} — "
            "DOMPurify (st.html unsafe_allow_javascript) va probablement "
            "supprimer tout le script silencieusement. Contenu:\n" + block
        )


class _FakeSessionState(dict):
    """dict suffit : .get() et __setitem__ sont tout ce que
    _broadcast_diff utilise sur st.session_state."""


class _HtmlCapture:
    """Remplace st.html : n'enregistre que les appels avec
    unsafe_allow_javascript=True (les seuls concernés)."""

    def __init__(self):
        self.bodies: list[str] = []

    def __call__(self, body, **kwargs):
        if kwargs.get("unsafe_allow_javascript"):
            self.bodies.append(str(body))


@pytest.fixture
def html_capture(monkeypatch):
    capture = _HtmlCapture()
    monkeypatch.setattr(debug_utils.st, "html", capture)
    monkeypatch.setattr(debug_utils.st, "markdown", lambda *a, **k: None)
    monkeypatch.setattr(debug_utils.st, "caption", lambda *a, **k: None)
    return capture


def test_source_script_blocks_have_no_literal_chevron():
    """Scan statique du fichier tel qu'écrit, limité aux arguments
    réellement passés à st.html(...) : attrape un tag HTML collé à la
    main dans un template, avant même d'exécuter quoi que ce soit."""
    source = DEBUG_UTILS_SRC.read_text(encoding="utf-8")
    templates = _html_call_template_texts(source)
    assert templates, "aucun appel st.html(...) trouvé dans debug_utils.py — le test ne vérifie plus rien"
    for template in templates:
        blocks = _script_blocks(template)
        if blocks:
            _assert_no_stray_chevron(blocks, source_label="debug_utils.py (template st.html, source statique)")


def test_console_page_script_is_clean(html_capture):
    debug_utils.render_debug_console_page()
    assert len(html_capture.bodies) == 1
    _assert_no_stray_chevron(
        _script_blocks(html_capture.bodies[0]),
        source_label="render_debug_console_page()",
    )


class _NoRepr:
    """Objet sans __repr__ custom : repr() par défaut de Python
    contient '<' et '>' nativement (ex: <....._NoRepr object at
    0x...>). Reproduit le cas réel le plus probable de '<' injecté
    dans le JSON du diff sans qu'aucune donnée "HTML" n'ait été
    stockée exprès dans session_state."""


@pytest.mark.parametrize(
    "poison_value",
    [
        "<a href='x'>lien</a>",
        "</span> injection",
        _NoRepr(),
    ],
    ids=["chaine-html", "fermeture-span", "repr-objet-par-defaut"],
)
def test_broadcast_diff_script_survives_adversarial_session_state(html_capture, poison_value):
    """_broadcast_diff() interpole du JSON (valeurs de session_state
    passées par _fmt_value/repr) directement dans le <script>. Si ce
    JSON contient un '<' non échappé, le bug revient au runtime même
    si le template lui-même est propre — cf. _json_for_script()."""
    debug_utils.st.session_state = _FakeSessionState()
    debug_utils._broadcast_diff(
        context="app.py",
        run_n=1,
        added={"poisoned_key": poison_value},
        removed={},
        changed={},
    )
    assert len(html_capture.bodies) == 1
    _assert_no_stray_chevron(
        _script_blocks(html_capture.bodies[0]),
        source_label="_broadcast_diff() (valeur adverse)",
    )


@pytest.mark.parametrize(
    "poison_value",
    ["<a href='x'>lien</a>", "</span>", _NoRepr()],
    ids=["chaine-html", "fermeture-span", "repr-objet-par-defaut"],
)
def test_json_for_script_escapes_without_losing_data(poison_value):
    """_json_for_script() doit neutraliser '<' pour le parseur HTML
    (aucun '<' littéral dans le texte produit) sans perdre
    l'information : JSON.parse() côté navigateur doit pouvoir
    retrouver la valeur d'origine. \\u003c est l'équivalent JSON
    exact de '<', donc on vérifie le round-trip côté Python avec
    json.loads (même parseur JSON, pas de navigateur nécessaire)."""
    original = {"added": {"k": debug_utils._fmt_value(poison_value)}}
    produced = debug_utils._json_for_script(original)

    assert "<" not in produced, "le '<' n'a pas été échappé"
    assert json.loads(produced) == original, "l'échappement a perdu ou altéré la donnée"
