"""
memia.debug_utils
------------------
Utilitaires de debug pour le développement local — inertes en
production. session_state est un objet 100% serveur Python : rien ici
ne l'expose côté navigateur par défaut (console DevTools, localStorage)
sauf appel explicite à mirror_to_browser_console().

Activation : MEMIA_DEBUG=1 streamlit run app.py
         ou : ajouter ?debug=1 dans l'URL de l'app en cours d'exécution
         (reste actif ensuite même après un switch_page, cf.
         is_debug_enabled ci-dessous)

Panneau pop-out : le bouton "Ouvrir dans un nouvel onglet" du panneau
sidebar ouvre un VRAI nouvel onglet Chrome → nouvelle session Streamlit,
donc session_state y est vide (cf. st.link_button, doc officielle :
"This will create a new session for the user"). Ce nouvel onglet ne
dépend donc PAS de session_state : il écoute les diffs de l'onglet
principal en live via BroadcastChannel, une API navigateur native de
communication entre onglets de même origine, sans repasser par le
serveur.
"""

import json
import os
import sys
import time

import streamlit as st

_SNAPSHOT_KEY = "__debug_session_state_snapshot__"
_RUN_COUNTER_KEY = "__debug_run_counter__"
_ENABLED_KEY = "__debug_enabled__"
_PANEL_EXPANDED_KEY = "__debug_panel_expanded__"
_HISTORY_KEY = "__debug_history__"
_HISTORY_MAX = 50
_MAX_VALUE_LEN = 80
_BROADCAST_CHANNEL_NAME = "memia-debug"

_COLOR_ENABLED = sys.stdout.isatty() and os.environ.get("NO_COLOR") != "1"


def _c(code: str, text: str) -> str:
    if not _COLOR_ENABLED:
        return text
    return f"\x1b[{code}m{text}\x1b[0m"


def _fmt_value(v) -> str:
    r = repr(v)
    if len(r) > _MAX_VALUE_LEN:
        r = r[:_MAX_VALUE_LEN - 1] + "…"
    return r


def _json_for_script(obj) -> str:
    """json.dumps, mais avec tout '<' littéral échappé en \\u003c.

    Un dict/liste de session_state peut contenir n'importe quelle
    chaîne (y compris avec des '<'), et json.dumps n'échappe PAS '<'
    par défaut. Cette fonction sert à interpoler du JSON dans le
    script inline passé à st.html(unsafe_allow_javascript=True) : ce
    contenu est sanitizé côté navigateur par DOMPurify, qui ne le
    traite PAS comme du texte brut — un '<' littéral n'importe où
    dedans (même caché dans une valeur JSON) peut faire sauter tout le
    script, silencieusement (cf. commentaires dans
    render_debug_console_page). \\u003c est une échappe JSON valide :
    JSON.parse() la redécode en '<' normalement côté JS, mais le texte
    SOURCE du script, lui, ne contient plus jamais le caractère '<'.
    """
    return json.dumps(obj).replace("<", "\\u003c")


def is_debug_enabled() -> bool:
    if _ENABLED_KEY not in st.session_state:
        enabled = (
            os.environ.get("MEMIA_DEBUG") == "1"
            or st.query_params.get("debug") == "1"
        )
        st.session_state[_ENABLED_KEY] = enabled

    if st.session_state[_ENABLED_KEY]:
        st.query_params["debug"] = "1"

    return st.session_state[_ENABLED_KEY]


def disable_debug():
    st.session_state[_ENABLED_KEY] = False
    if "debug" in st.query_params:
        del st.query_params["debug"]


def _current_state() -> dict:
    internal_keys = (_SNAPSHOT_KEY, _RUN_COUNTER_KEY, _ENABLED_KEY, _PANEL_EXPANDED_KEY, _HISTORY_KEY)
    return {k: v for k, v in st.session_state.items() if k not in internal_keys}


def _compute_diff():
    current = _current_state()
    previous = st.session_state.get(_SNAPSHOT_KEY, {})
    run_n = st.session_state.get(_RUN_COUNTER_KEY, 0) + 1
    st.session_state[_RUN_COUNTER_KEY] = run_n

    added = {k: v for k, v in current.items() if k not in previous}
    removed = {k: v for k, v in previous.items() if k not in current}
    changed = {
        k: (previous[k], v)
        for k, v in current.items()
        if k in previous and previous[k] != v
    }
    st.session_state[_SNAPSHOT_KEY] = dict(current)
    return added, removed, changed, run_n


def log_session_state(context: str = ""):
    """
    Log dans le TERMINAL le diff (uniquement les clés changées), et le
    diffuse en parallèle vers un éventuel onglet de debug ouvert à part
    (cf. render_debug_console_page).
    """
    if not is_debug_enabled():
        return

    added, removed, changed, run_n = _compute_diff()
    if not (added or removed or changed):
        return

    label = f" {context} " if context else " "
    header = f"session_state{label}· run #{run_n}"
    width = max(60, len(header) + 4)
    print(_c("2", "─" * 2) + " " + _c("1;36", header) + " " + _c("2", "─" * (width - len(header) - 4)))

    key_width = max([len(k) for k in (*added, *removed, *changed)], default=0)
    for k, v in added.items():
        print(f"  {_c('32', '+')} {k.ljust(key_width)}  {_c('32', _fmt_value(v))}")
    for k, v in removed.items():
        print(f"  {_c('31', '-')} {k.ljust(key_width)}  {_c('2', 'était ' + _fmt_value(v))}")
    for k, (old, new) in changed.items():
        print(f"  {_c('33', '~')} {k.ljust(key_width)}  {_fmt_value(old)} {_c('33', '→')} {_fmt_value(new)}")
    print(_c("2", "─" * width))

    _broadcast_diff(context, run_n, added, removed, changed)


def _broadcast_diff(context, run_n, added, removed, changed):
    entry = {
        "context": context,
        "run": run_n,
        "timestamp": time.strftime("%H:%M:%S"),
        "added": {k: _fmt_value(v) for k, v in added.items()},
        "removed": {k: _fmt_value(v) for k, v in removed.items()},
        "changed": {k: [_fmt_value(o), _fmt_value(n)] for k, (o, n) in changed.items()},
    }

    history = st.session_state.get(_HISTORY_KEY, [])
    history.append(entry)
    if len(history) > _HISTORY_MAX:
        history = history[-_HISTORY_MAX:]
    st.session_state[_HISTORY_KEY] = history

    try:
        entry_json = _json_for_script(entry)
        history_json = _json_for_script(history)
    except TypeError:
        return

    # Le <script> est réinjecté à CHAQUE run (st.html) : on garde le
    # canal singleton via window.__memiaDebugChannel pour ne pas en
    # recréer un à chaque rerun, mais on RÉASSIGNE .onmessage à chaque
    # fois pour que la réponse à 'request_snapshot' embarque toujours
    # l'historique le plus frais (closure sur `history_json` de CE run).
    st.html(f"""
    <script>
    (function() {{
        if (!('BroadcastChannel' in window)) return;
        if (!window.__memiaDebugChannel) {{
            window.__memiaDebugChannel = new BroadcastChannel('{_BROADCAST_CHANNEL_NAME}');
        }}
        const bc = window.__memiaDebugChannel;
        const history = {history_json};

        bc.onmessage = (e) => {{
            if (e.data && e.data.type === 'request_snapshot') {{
                bc.postMessage({{ type: 'history', history: history }});
            }}
        }};

        bc.postMessage({{ type: 'entry', entry: {entry_json} }});
    }})();
    </script>
    """, unsafe_allow_javascript=True)


def render_debug_panel():
    if not is_debug_enabled():
        return
    with st.sidebar:
        expanded = st.session_state.get(_PANEL_EXPANDED_KEY, False)
        with st.expander("🐛 session_state (debug)", expanded=expanded):
            st.session_state[_PANEL_EXPANDED_KEY] = True
            st.json(_current_state())
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Désactiver", key="__debug_disable_btn__"):
                    disable_debug()
                    st.rerun()
            with col2:
                st.link_button(
                    "↗ Nouvel onglet",
                    "?debug=1&debug_console=1",
                    key="__debug_open_console_btn__",
                )


def render_debug_console_page():
    """
    Page pop-out — appelée depuis app.py quand ?debug_console=1 est
    présent, AVANT le routing normal (st.navigation/pages.run). Ne lit
    ni n'écrit session_state pour son affichage: tout repose sur
    BroadcastChannel, car cet onglet est une session Streamlit à part
    entière, distincte de celle de l'onglet principal.
    """
    st.markdown("### 🐛 MemIA — Panneau de debug (session_state)")
    st.caption(
        "Miroir live de session_state depuis l'onglet principal, via "
        "BroadcastChannel"
    )
    st.html(f"""
    <div style="margin-bottom:8px; display:flex; align-items:center; gap:12px;">
        <button id="memia-debug-clear" style="
            background:#21262d; color:#c9d1d9; border:1px solid #30363d;
            border-radius:6px; padding:4px 12px; cursor:pointer; font-size:13px;
        ">Effacer</button>
        <span id="memia-debug-status" style="font-size:13px; color:#8b949e;">
            En attente de l'onglet principal…
        </span>
    </div>
    <div id="memia-debug-log" style="
        font-family: 'SFMono-Regular', Consolas, monospace;
        font-size: 13px; line-height: 1.6;
        background: #0d1117; color: #c9d1d9;
        border-radius: 8px; padding: 12px;
        height: 70vh; overflow-y: auto; white-space: pre-wrap;
    "></div>
    <script>
    (function() {{
        if (!('BroadcastChannel' in window)) {{
            document.getElementById('memia-debug-log').textContent =
                "BroadcastChannel non supporté par ce navigateur.";
            return;
        }}
        const bc = new BroadcastChannel('{_BROADCAST_CHANNEL_NAME}');
        const logEl = document.getElementById('memia-debug-log');
        const statusEl = document.getElementById('memia-debug-status');

        // ATTENTION en modifiant ce bloc : ceci est un script inline
        // rendu via st.html(unsafe_allow_javascript=True), sanitizé
        // côté navigateur par DOMPurify avant exécution. Ce sanitizer
        // ne traite PAS ce contenu comme du texte brut — un chevron
        // ouvrant, où qu'il apparaisse (code, string JS, ou commentaire,
        // fermé ou non), est lu comme une balise et peut faire passer
        // le résultat sanitizé à vide (aucune erreur JS, juste un
        // onglet de debug muet). D'où la construction du log via
        // createElement/textContent plutôt que des strings HTML
        // concaténées : aucun chevron littéral dans ce script, donc
        // rien pour le sanitizer à mal interpréter.
        function chip(text, color) {{
            const el = document.createElement('span');
            if (color) el.style.color = color;
            el.textContent = text;
            return el;
        }}

        function renderEntry(entry) {{
            statusEl.textContent = 'Connecté — dernier run #' + entry.run;
            statusEl.style.color = '#3fb950';

            const div = document.createElement('div');
            div.appendChild(chip(
                '── ' + (entry.context || '') + ' · run #' + entry.run +
                ' · ' + entry.timestamp + ' ──',
                '#8b949e'
            ));
            div.appendChild(document.createTextNode('\\n'));
            for (const [k, v] of Object.entries(entry.added || {{}})) {{
                div.appendChild(chip('+', '#3fb950'));
                div.appendChild(document.createTextNode(' ' + k + '  '));
                div.appendChild(chip(v, '#3fb950'));
                div.appendChild(document.createTextNode('\\n'));
            }}
            for (const [k, v] of Object.entries(entry.removed || {{}})) {{
                div.appendChild(chip('-', '#f85149'));
                div.appendChild(document.createTextNode(' ' + k + '  '));
                div.appendChild(chip('était ' + v, '#8b949e'));
                div.appendChild(document.createTextNode('\\n'));
            }}
            for (const [k, ov] of Object.entries(entry.changed || {{}})) {{
                div.appendChild(chip('~', '#d29922'));
                div.appendChild(document.createTextNode(' ' + k + '  ' + ov[0] + ' '));
                div.appendChild(chip('→', '#d29922'));
                div.appendChild(document.createTextNode(' ' + ov[1] + '\\n'));
            }}
            logEl.appendChild(div);
            logEl.scrollTop = logEl.scrollHeight;
        }}

        bc.onmessage = (e) => {{
            if (!e.data) return;
            if (e.data.type === 'entry') {{
                renderEntry(e.data.entry);
            }} else if (e.data.type === 'history') {{
                (e.data.history || []).forEach(renderEntry);
            }}
        }};

        document.getElementById('memia-debug-clear').onclick = () => {{
            logEl.innerHTML = '';
        }};

        // Rattrapage : redemande l'historique à l'onglet principal,
        // car BroadcastChannel ne rejoue jamais les messages envoyés
        // avant l'ouverture de CET onglet.
        bc.postMessage({{ type: 'request_snapshot' }});
    }})();
    </script>
    """, unsafe_allow_javascript=True)