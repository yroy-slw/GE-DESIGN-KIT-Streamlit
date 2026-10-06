"""
ge_design_kit.topbar
----------------------
Bandeau GE plein-largeur, positionné AU-DESSUS de la sidebar ET du
contenu principal (position: fixed sur tout le viewport) — reproduit
le header MemIA du Figma (node 558:2339, "CHA_Header") : liseré bleu
primary en haut, bouton burger + nom d'app/badge d'environnement à
gauche, compte utilisateur à droite.

Le burger ne pilote PAS le collapse natif de st.sidebar (qui ne sait
que montrer/cacher en entier, pas un mode rail à largeur
intermédiaire) : il remonte un trigger CCv2 (pattern
setTriggerValue/on_<nom>_change, identique à ge_sidebar) que
l'appelant (app.py) relie à un callback `on_toggle` qui bascule
st.session_state.sidebar_collapsed — c'est ce flag qui pilote à la
fois la largeur de section[data-testid="stSidebar"] (cf.
layout.py: inject_ge_layout(sidebar_collapsed=...)) et le rendu rail
de ge_sidebar (cf. sidebar.py: ge_sidebar(collapsed=...)).
"""

import streamlit as st
from .icons import ICON_FONT_CSS

# Source de vérité unique pour la hauteur — réutilisée dans layout.py
# pour pousser la sidebar/le contenu vers le bas du même montant.
TOPBAR_HEIGHT_PX = 81

# Hauteur du liseré de couleur primary en haut du bandeau (Figma: 8px).
_ACCENT_HEIGHT_PX = 8

_ge_topbar = st.components.v2.component(
    name="ge_topbar",
    html="""
    <header class="ge-topbar">
        <div class="ge-topbar-accent"></div>
        <div class="ge-topbar-left">
            <button type="button" class="ge-topbar-burger" id="ge-topbar-burger" aria-label="Afficher/masquer le menu">
                <span class="material-symbols-outlined">menu</span>
            </button>
            <div class="ge-topbar-brand">
                <span class="ge-topbar-name" id="ge-topbar-name"></span>
                <span class="ge-topbar-env" id="ge-topbar-env"></span>
            </div>
        </div>
        <div class="ge-topbar-user">
            <span class="material-symbols-outlined ge-topbar-user-icon">person</span>
            <span class="ge-topbar-user-label" id="ge-topbar-user-label"></span>
        </div>
    </header>
    """,
    css=ICON_FONT_CSS + f"""
    .ge-topbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: {TOPBAR_HEIGHT_PX}px;
        background: var(--md-sys-color-surface);
        border-bottom: 1px solid var(--md-sys-color-outline-variant);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: {_ACCENT_HEIGHT_PX}px calc(var(--spacing) * 8) 0;
        box-sizing: border-box;
        z-index: 999999;
        font-family: var(--st-font, sans-serif);
    }}
    .ge-topbar-accent {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: {_ACCENT_HEIGHT_PX}px;
        background: var(--md-sys-color-primary);
    }}
    .ge-topbar-left {{
        display: flex;
        align-items: center;
        gap: calc(var(--spacing) * 6);
        height: 100%;
    }}
    .ge-topbar-burger {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        border: none;
        background: transparent;
        padding: 8px;
        margin: -8px;
        border-radius: 50%;
        color: var(--md-sys-color-on-surface);
        cursor: pointer;
        transition: background 0.12s;
    }}
    .ge-topbar-burger:hover {{
        background: color-mix(in srgb, var(--md-sys-color-on-surface) 8%, transparent);
    }}
    .ge-topbar-burger .material-symbols-outlined {{
        font-size: 35px;
    }}
    .ge-topbar-brand {{
        display: flex;
        align-items: baseline;
        gap: calc(var(--spacing) * 2);
        height: auto;
    }}
    .ge-topbar-name {{
        font-family: var(--md-ref-typeface-brand, Roboto, sans-serif);
        font-size: 28px;
        font-weight: 600;
        color: var(--md-sys-color-on-surface);
        line-height: 1;
    }}
    .ge-topbar-env {{
        font-family: var(--md-ref-typeface-brand, Roboto, sans-serif);
        font-size: 28px;
        font-weight: 400;
        color: var(--md-sys-color-on-surface);
        line-height: 1;
    }}
    .ge-topbar-env:empty {{
        display: none;
    }}
    .ge-topbar-user {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 2px;
        min-width: 68px;
        padding: calc(var(--spacing) * 4) 0;
        color: var(--md-sys-color-on-surface-variant);
        margin-right: 100px;
    }}
    .ge-topbar-user-icon {{
        font-size: 35px;
    }}
    .ge-topbar-user-label {{
        font-size: var(--md-sys-typescale-body-small-size);
        letter-spacing: var(--md-sys-typescale-body-small-tracking);
    }}
    """,
    js="""
    export default function({ parentElement, data, setTriggerValue }) {
        parentElement.querySelector('#ge-topbar-name').textContent = data.app_name;
        parentElement.querySelector('#ge-topbar-env').textContent = data.env || '';
        parentElement.querySelector('#ge-topbar-user-label').textContent = data.user_label;

        // Date.now() plutôt qu'un simple booléen/compteur: garantit une
        // valeur DIFFÉRENTE à chaque clic, donc une détection de
        // changement fiable même si l'utilisateur veut re-déclencher le
        // même état deux fois de suite (cf. ge_sidebar pour le même
        // pattern setTriggerValue/on_<nom>_change).
        parentElement.querySelector('#ge-topbar-burger').onclick = () => {
            setTriggerValue('toggled', Date.now());
        };
    }
    """,
)


def ge_topbar(
    app_name: str = "GE",
    user_label: str = "Mon compte",
    env: str | None = None,
    on_toggle=None,
):
    """
    Affiche le bandeau GE plein-largeur, fixé en haut de la fenêtre,
    avec un bouton burger à gauche.

    env: badge d'environnement optionnel affiché juste après app_name
    (ex: "DEV", "TEST") — masqué si None/vide.
    on_toggle: callback appelé à chaque clic sur le burger (sans
    argument) — c'est à l'appelant de décider ce que "toggle" signifie
    (cf. app.py: bascule st.session_state.sidebar_collapsed, qui pilote
    ensuite layout.py et ge_sidebar). Ne fait rien si omis.
    """
    _ge_topbar(
        key="ge_topbar",
        data={
            "app_name": app_name,
            "user_label": user_label,
            "env": env or "",
        },
        on_toggled_change=on_toggle if on_toggle is not None else lambda: None,
    )