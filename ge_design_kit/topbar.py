"""
ge_design_kit.topbar
----------------------
Bandeau GE plein-largeur, positionné AU-DESSUS de la sidebar ET du
contenu principal (position: fixed sur tout le viewport) — reproduit
le topbar GE de nos wireframes SuisseVote/MemIA (logo + "Mon compte").
"""

import streamlit as st
from .icons import ICON_FONT_CSS

# Source de vérité unique pour la hauteur — réutilisée dans layout.py
# pour pousser la sidebar/le contenu vers le bas du même montant.
TOPBAR_HEIGHT_PX = 81

_LOGO_PATH = "assets/logo-ge.svg"


def _load_logo_svg() -> str:
    """
    Lit le SVG du logo GE officiel depuis le disque. En cas d'absence
    du fichier (mauvais chemin, pas encore copié...), on dégrade
    proprement vers un simple carré de substitution plutôt que de
    planter l'app entière.
    """
    try:
        with open(_LOGO_PATH, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return '<div style="width:28px;height:28px;background:#ccc;border-radius:4px;"></div>'


_ge_topbar = st.components.v2.component(
    name="ge_topbar",
    html="""
    <header class="ge-topbar">
        <div class="ge-topbar-brand">
            <div class="ge-topbar-coat" id="ge-topbar-coat"></div>
            <span class="ge-topbar-name" id="ge-topbar-name"></span>
        </div>
        <div class="ge-topbar-user">
            <span class="material-symbols-outlined ge-topbar-user-icon">account_circle</span>
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
        padding: 0 calc(var(--spacing) * 6);
        box-sizing: border-box;
        z-index: 999999;
        font-family: var(--st-font, sans-serif);
    }}
    .ge-topbar-brand {{
        display: flex;
        align-items: center;
        gap: calc(var(--spacing) * 3);
        height: 100%;
    }}
    .ge-topbar-coat {{
        display: flex;
        align-items: center;
        flex-shrink: 0;
    }}
    .ge-topbar-coat svg {{
        width: 28px !important;
        height: 45px !important;
        display: block;
    }}
    .ge-topbar-name {{
        font-family: var(--md-ref-typeface-brand, Roboto, sans-serif);
        font-size: 28px;
        font-weight: 400;
        text-transform: uppercase;
        color: var(--md-sys-color-on-surface);
        line-height: 1;
    }}
    .ge-topbar-user {{
        display: flex;
        align-items: center;
        gap: calc(var(--spacing) * 2);
        color: var(--md-sys-color-on-surface-variant);
        margin-right: 100px;
    }}
    .ge-topbar-user-icon {{
        font-size: 26px;
    }}
    .ge-topbar-user-label {{
        font-size: var(--md-sys-typescale-label-medium-size);
    }}
    """,
    js="""
    export default function({ parentElement, data }) {
        const coat = parentElement.querySelector('#ge-topbar-coat');
        coat.innerHTML = data.logo_svg;
        const svg = coat.querySelector('svg');
        if (svg) {
            svg.setAttribute('width', '28');
            svg.setAttribute('height', '45');
        }
        parentElement.querySelector('#ge-topbar-name').textContent = data.app_name;
        parentElement.querySelector('#ge-topbar-user-label').textContent = data.user_label;
    }
    """,
)


def ge_topbar(app_name: str = "GE", user_label: str = "Mon compte"):
    """
    Affiche le bandeau GE plein-largeur, fixé en haut de la fenêtre.
    """
    _ge_topbar(
        key="ge_topbar",
        data={
            "app_name": app_name,
            "user_label": user_label,
            "logo_svg": _load_logo_svg(),
        },
    )