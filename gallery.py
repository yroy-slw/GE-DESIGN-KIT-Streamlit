"""
Galerie de composants GE-Design-kit — outil de développement autonome,
PAS une page de l'app MemIA (app.py a sa propre navigation simulée via
ge_sidebar + session_state, pas de vraie navigation multipage
Streamlit — cf. sa docstring). Se lance séparément :

    streamlit run gallery.py

Chaque section montre le rendu réel du composant ET le code Python
exact qui l'a produit (via inspect.getsource — le snippet affiché ne
peut donc jamais diverger silencieusement de ce qui a vraiment tourné).
"""

import inspect
import textwrap

import streamlit as st

from ge_design_kit import (
    inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar, ge_breadcrumb, ge_surface,
    ge_card, ge_kpi, ge_sidebar, ge_label_spacer,
    FILLED_BUTTON_KEY_PREFIX, ICON_BUTTON_KEY_PREFIX, OUTLINED_BUTTON_KEY_PREFIX,
    TEXT_BUTTON_KEY_PREFIX, GE_TOGGLE_KEY_PREFIX,
)

st.set_page_config(page_title="GE-Design-kit — Galerie de composants", layout="wide")
inject_ge_styles()

with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="GE", user_label="Galerie")

# st.logo() n'est pas que de la marque : c'est aussi CE QUI PERMET DE
# RÉ-EXPANDRE la sidebar une fois repliée (clic sur le logo réinjecté
# dans le header natif). Sans lui, une fois la sidebar collapsed sur
# cette page, impossible de la rouvrir. Wordmark dédié ("Design", même
# style typographique que assets/memia_logo.svg) plutôt que réutiliser
# le logo MemIA — cette page n'est pas l'app MemIA.
st.logo("assets/design_logo.svg", size="small")
# size="small" le rend un peu petit comparé au logo MemIA de l'app —
# ajustement direct, scopé à CETTE page seulement (gallery.py est un
# script Streamlit à part, jamais exécuté par app.py, donc ça ne
# touche pas le logo MemIA). Cible les deux testid — stSidebarLogo
# (sidebar ouverte) ET stHeaderLogo (sidebar repliée, cf. commentaire
# ci-dessus) — sinon la taille redeviendrait incohérente une fois
# collapsed.
st.html("""
<style>
[data-testid="stSidebarLogo"],
[data-testid="stHeaderLogo"] {
    height: 1.85rem !important;
    width: auto !important;
}
</style>
""")


def show_example(func):
    """
    Exécute `func()` (le rendu réel du composant) puis affiche son
    propre code source en dessous, dédenté et sans la ligne `def ...:`
    — un snippet directement copiable dans une vraie app.
    """
    func()
    source = inspect.getsource(func)
    lines = source.splitlines()[1:]  # retire la ligne "def demo_xxx():"
    body = textwrap.dedent("\n".join(lines))
    st.code(body, language="python")


st.title("Galerie de composants GE-Design-kit")
st.caption(
    "Référence visuelle + code d'intégration pour chaque composant du kit. "
    "Lancé séparément de l'app (`streamlit run gallery.py`) — voir le "
    "README du kit pour la doc complète de chaque fonction."
)

# ── Sommaire (ancres natives st.header) ──────────────────────────────
st.markdown(
    "**Sommaire :** "
    "[Topbar](#topbar) · [Sidebar](#sidebar) · [Breadcrumb](#breadcrumb) · "
    "[Surface](#surface) · [Card](#card) · [KPI](#kpi) · "
    "[Boutons](#boutons) · [Checkbox et Toggle](#checkbox-et-toggle) · "
    "[Modal](#modal) · [Alertes](#alertes) · "
    "[Typographie](#typographie) · "
    "[Widgets natifs stylés](#widgets-natifs-stylés-automatiquement)"
)
st.divider()

# ── Topbar ────────────────────────────────────────────────────────────
st.header("Topbar", anchor="topbar")
st.write(
    "Bandeau institutionnel fixe en haut de l'app. Déjà affiché tout en "
    "haut de cette page — voir le code ci-dessous."
)


def demo_ge_topbar():
    from ge_design_kit import inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar

    st.set_page_config(page_title="Mon app", layout="wide")
    inject_ge_styles()  # une seule fois, tout en haut de l'app

    with st.container(key=TOPBAR_SLOT_KEY):
        ge_topbar(app_name="GE", user_label="Mon compte")


st.code(
    textwrap.dedent("\n".join(inspect.getsource(demo_ge_topbar).splitlines()[1:])),
    language="python",
)
st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────
st.header("Sidebar", anchor="sidebar")
st.write(
    "Menu latéral de navigation — utilisé dans `st.sidebar` de cette même "
    "page (regardez à gauche). Retourne l'id de l'item cliqué durant CE "
    "run (ou `None`), à combiner avec `st.session_state` pour piloter la "
    "page active."
)

with st.sidebar:
    gallery_selected = ge_sidebar(
        items=[
            {"id": "operation", "label": "Composants", "icon": "computer"},
        ],
        active_id="operation",
        key="gallery_sidebar",
    )


def demo_ge_sidebar():
    with st.sidebar:
        selected = ge_sidebar(
            items=[
                {"id": "operation", "label": "Opération", "icon": "add_circle"},
                {"id": "configuration", "label": "Configuration", "icon": "settings"},
                {"divider": True},
                {"id": "analyse", "label": "Analyse", "icon": "scatter_plot", "has_children": True},
                {"id": "recherche", "label": "Recherche", "icon": "search"},
            ],
            active_id=st.session_state.current_page,
            key="main_sidebar",
        )
        if selected:
            st.session_state.current_page = selected
            st.rerun()


st.code(
    textwrap.dedent("\n".join(inspect.getsource(demo_ge_sidebar).splitlines()[1:])),
    language="python",
)
st.divider()

# ── Breadcrumb ────────────────────────────────────────────────────────
st.header("Breadcrumb", anchor="breadcrumb")


def demo_ge_breadcrumb():
    ge_breadcrumb(items=[
        {"id": "home", "label": "Accueil"},
        {"id": "operations", "label": "Sélectionner une opération"},
    ])


show_example(demo_ge_breadcrumb)
st.divider()

# ── Surface ───────────────────────────────────────────────────────────
st.header("Surface", anchor="surface")
st.write(
    "Conteneur de page - contrairement à `ge_card`, peut contenir "
    "n'importe quel widget Streamlit. Deux variantes : `\"card\"` "
    "(fond blanc + ombre, défaut) et `\"inset\"` (fond teinté, sans "
    "ombre, pour sous-grouper du contenu dans une carte)."
)


def demo_ge_surface():
    with ge_surface("gallery-demo-surface"):
        st.write("Contenu dans une surface variant=\"card\" (défaut).")
        with ge_surface("gallery-demo-inset", variant="inset"):
            st.write("Sous-bloc en variant=\"inset\".")


show_example(demo_ge_surface)
st.divider()

# ── Card ──────────────────────────────────────────────────────────────
st.header("Card", anchor="card")
st.write(
    "Composant CCv2 figé (titre + texte + bouton optionnel) — ne peut "
    "PAS contenir d'autres widgets Streamlit (contrairement à "
    "`ge_surface`). Retourne `True` le run où le bouton est cliqué."
)


def demo_ge_card():
    clicked = ge_card(
        "Opérations",
        "4 disponibles",
        icon="📋",
        button_label="Voir",
        key="gallery_card",
    )
    if clicked:
        st.toast("Carte cliquée !")


show_example(demo_ge_card)
st.divider()

# ── KPI ───────────────────────────────────────────────────────────────
st.header("KPI", anchor="kpi")
st.write("Card chiffre + libellé, purement d'affichage (pas d'interaction).")


def demo_ge_kpi():
    c1, c2, c3 = st.columns(3)
    with c1:
        ge_kpi(4, "Opérations disponibles", key="gallery_kpi_1")
    with c2:
        ge_kpi(0, "Analyses terminées", key="gallery_kpi_2")
    with c3:
        ge_kpi(1, "Analyse en cours", key="gallery_kpi_3")


show_example(demo_ge_kpi)
st.caption(
    "Le 2ᵉ exemple vaut délibérément 0 — `ge_kpi` gère bien ce cas "
    "(un ancien bug affichait `0` comme une chaîne vide, cf. forms.py)."
)
st.divider()

# ── Boutons ───────────────────────────────────────────────────────────
st.header("Boutons", anchor="boutons")
st.write(
    "`st.button()` n'accepte pas de classe CSS personnalisée : le style "
    "passe par un **conteneur enveloppant** (`st.container(key=...)`), "
    "pas par le bouton lui-même. Quatre variantes, vocabulaire Material "
    "Design 3 :"
)
st.markdown(
    "- `FILLED_BUTTON_KEY_PREFIX` — fond plein couleur primary, libellé "
    "(ex : action principale d'un écran, \"Télécharger en CSV\")\n"
    "- `ICON_BUTTON_KEY_PREFIX` — bouton rond, icône seule, fond plein "
    "couleur primary (ex : bouton recherche rond)\n"
    "- `OUTLINED_BUTTON_KEY_PREFIX` — contour fin, fond transparent "
    "(ex : action secondaire)\n"
    "- `TEXT_BUTTON_KEY_PREFIX` — pas de bordure ni de fond, libellé "
    "coloré (ex : action discrète)"
)


def demo_buttons():
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}gallery_filled"):
            st.button("Télécharger", icon=":material/file_download:", key="gallery_btn_filled")
    with b2:
        with st.container(key=f"{ICON_BUTTON_KEY_PREFIX}gallery_icon"):
            st.button("", icon=":material/search:", key="gallery_btn_icon")
    with b3:
        with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_outlined"):
            st.button("Importer", icon=":material/upload:", key="gallery_btn_outlined")
    with b4:
        with st.container(key=f"{TEXT_BUTTON_KEY_PREFIX}gallery_text"):
            st.button("Annuler", icon=":material/close:", key="gallery_btn_text")


show_example(demo_buttons)
st.divider()

st.subheader("ge_label_spacer")
st.write(
    "`st.button` n'a pas de label au-dessus de lui, contrairement à "
    "`text_input`/`selectbox` — côte à côte, le bouton se retrouve plus "
    "haut que ses voisins. `ge_label_spacer(height_px=10)` comble cet "
    "écart. Comparaison, sans puis avec :"
)


def demo_label_spacer():
    s1, s2 = st.columns(2)
    with s1:
        st.caption("Sans spacer — mal aligné")
        a1, a2 = st.columns([3, 1])
        with a1:
            st.text_input("Champ", key="gallery_spacer_input_bad")
        with a2:
            with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_bad"):
                st.button("OK", key="gallery_btn_bad")
    with s2:
        st.caption("Avec spacer — aligné")
        b1, b2 = st.columns([3, 1])
        with b1:
            st.text_input("Champ", key="gallery_spacer_input_good")
        with b2:
            with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_good"):
                ge_label_spacer()
                st.button("OK", key="gallery_btn_good")


show_example(demo_label_spacer)
st.divider()

# ── Checkbox et Toggle ────────────────────────────────────────────────
st.header("Checkbox et Toggle", anchor="checkbox-et-toggle")
st.write(
    "`st.checkbox` et `st.toggle` sont le **même composant** côté "
    "Streamlit (même `data-testid`). Un `st.checkbox` **non enveloppé** "
    "s'affiche en case à cocher standard par défaut — c'est "
    "`st.toggle` qui a besoin d'être explicitement enveloppé dans "
    "`GE_TOGGLE_KEY_PREFIX` pour devenir un switch, sinon il "
    "hériterait de l'apparence case-à-cocher."
)


def demo_checkbox_toggle():
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Case à cocher standard", value=True, key="gallery_checkbox")
    with col2:
        with st.container(key=f"{GE_TOGGLE_KEY_PREFIX}gallery_toggle"):
            st.toggle("Interrupteur (switch)", value=True, key="gallery_toggle")


show_example(demo_checkbox_toggle)
st.divider()

# ── Modal ─────────────────────────────────────────────────────────────
st.header("Modal", anchor="modal")
st.write(
    "`st.dialog(...)` est un **décorateur** natif Streamlit (pas de "
    "CCv2 ici, comme les widgets ci-dessus) : on écrit une fonction, on "
    "l'appelle depuis un handler de clic, Streamlit affiche son contenu "
    "dans un overlay stylé GE-DESIGN automatiquement une fois "
    "`inject_ge_styles()` appelé — fond, coins, ombre, typographie du "
    "titre (cf. `ge_design_kit/dialog.py`, Figma node 120:4191). Un "
    "seul dialog ouvert à la fois ; ESC / clic-dehors / croix de "
    "fermeture sont gérés nativement."
)


@st.dialog("Titre du modal")
def _gallery_dialog():
    st.write("Contenu du dialog — n'importe quel widget Streamlit.")


def demo_dialog():
    with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}gallery_dialog"):
        if st.button("Ouvrir le modal", key="gallery_btn_dialog"):
            _gallery_dialog()


show_example(demo_dialog)
st.divider()

# ── Alertes ───────────────────────────────────────────────────────────
st.header("Alertes", anchor="alertes")
st.write(
    "`st.info`/`st.success`/`st.warning`/`st.error` — stylés "
    "automatiquement une fois `inject_ge_styles()`. Habillage GE-DESIGN \"MD_Stacked card_info\""
)


def demo_alerts():
    st.info(
        "Uniquement les appartements non meublés en immeuble.",
        title="Périmètre de la statistique",
    )
    st.success("Analyse terminée avec succès.")
    st.warning("Vérifiez les données avant de continuer.")
    st.error("Une erreur est survenue lors du traitement.")


show_example(demo_alerts)
st.divider()

# ── Typographie ───────────────────────────────────────────────────────
st.header("Typographie", anchor="typographie")
st.write(
    "Titres natifs Streamlit stylés automatiquement une fois "
    "`inject_ge_styles()` appelé — aucun conteneur enveloppant "
    "nécessaire. `layout.py` ajuste line-height/letter-spacing/padding "
    "sur `h1`/`h2`/`h3` directement (pas d'équivalent dans "
    "`.streamlit/config.toml` pour ce niveau de détail) : `st.title` → "
    "`h1` (typescale `headline-large`), `st.header` → `h2` (typescale "
    "`headline-small`, **partagée avec `st.subheader` → `h3`**)."
)


def demo_typography():
    st.title("Titre principal (st.title)")
    st.header("Titre de section (st.header)")


show_example(demo_typography)
st.divider()

# ── Widgets natifs stylés automatiquement ────────────────────────────
st.header("Widgets natifs stylés automatiquement", anchor="widgets-natifs-stylés-automatiquement")
st.write(
    "Une fois `inject_ge_styles()` appelé, ces widgets Streamlit natifs "
    "sont stylés GE-Design automatiquement — aucun conteneur "
    "enveloppant nécessaire, contrairement aux boutons et au toggle "
    "ci-dessus."
)


def demo_native_widgets():
    n1, n2 = st.columns(2)
    with n1:
        st.text_input("Champ texte", placeholder="Rechercher...", key="gallery_text_input")
    with n2:
        st.selectbox("Menu déroulant", options=["Tous", "Option A", "Option B"], key="gallery_selectbox")


show_example(demo_native_widgets)
st.caption(
    "**Non stylable** : `st.dataframe` (rendu sur `<canvas>`, pas de "
    "CSS possible — voir app.py pour le tableau des opérations, qui "
    "reste volontairement natif pour cette raison)."
)
