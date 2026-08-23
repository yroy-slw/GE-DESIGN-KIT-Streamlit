"""
ge_design_kit.layout
----------------------
Neutralise les contraintes de layout par défaut de Streamlit
(conteneur centré avec max-width) et restyle le st.sidebar
natif aux couleurs GE-DESIGN — plutôt que de simuler une sidebar
avec st.columns.
"""

import streamlit as st
from .topbar import TOPBAR_HEIGHT_PX

# Clé utilisée pour wrapper l'appel à ge_topbar() dans app.py — doit
# matcher exactement st.container(key=TOPBAR_SLOT_KEY) côté app.py.
TOPBAR_SLOT_KEY = "ge_topbar_slot"

# Padding vertical du header de la sidebar (zone logo + bouton collapse).
# Ajuste ces deux valeurs directement pour resserrer/espacer.
SIDEBAR_HEADER_PADDING_TOP_PX = 30
SIDEBAR_HEADER_PADDING_BOTTOM_PX = 0
SIDEBAR_HEADER_PADDING_LEFT_PX = 12

_LAYOUT_CSS_BODY = f"""
/* ── Menu natif Streamlit : pas masqué (on garde toolbarMode), ──
   ── repositionné pour se superposer à la bande topbar ── */
[data-testid="stHeader"] {{
    background: transparent !important;
    top: 0 !important;
    height: {TOPBAR_HEIGHT_PX}px !important;
    z-index: 1000000 !important; /* au-dessus de notre .ge-topbar (999999) */
}}

/* ── Slot contenant notre ge_topbar() : collapse sa hauteur de flux, ──
   ── le contenu reste visible grâce à position:fixed + overflow visible ── */
.st-key-{TOPBAR_SLOT_KEY} {{
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}}

/* ── Sidebar native : restyle GE-DESIGN + décalée sous notre topbar ── */
section[data-testid="stSidebar"] {{
    background: var(--md-sys-color-surface-container-low);
    border-right: 1px solid var(--md-sys-color-outline-variant);
    width: 260px !important;
    top: {TOPBAR_HEIGHT_PX}px !important;
    height: calc(100vh - {TOPBAR_HEIGHT_PX}px) !important;
}}
section[data-testid="stSidebar"] > div {{
    padding-top: 0;
}}

/* ── Header sidebar (logo + bouton collapse) : padding ajustable ── */
[data-testid="stSidebarHeader"] {{
    padding-top: {SIDEBAR_HEADER_PADDING_TOP_PX}px !important;
    padding-bottom: {SIDEBAR_HEADER_PADDING_BOTTOM_PX}px !important;
    padding-left: {SIDEBAR_HEADER_PADDING_LEFT_PX}px !important;
}}

/* ── Contenu principal : plein-largeur, pas de centrage, décalé sous le topbar ── */
.block-container,
[data-testid="stMainBlockContainer"] {{
    max-width: 100% !important;
    padding-top: calc({TOPBAR_HEIGHT_PX}px + var(--spacing) * 2) !important;
    padding-left: calc(var(--spacing) * 8) !important;
    padding-right: calc(var(--spacing) * 8) !important;
}}

[data-testid="stAppViewContainer"] {{
    background: var(--md-sys-color-surface);
}}

/* ── Line-height des titres : pas d'équivalent config.toml, ──
   ── donc CSS scopé strictement sur h1/h2/h3 (pas de sélecteur global) ── */
h1 {{
    line-height: var(--md-sys-typescale-headline-large-line-height) !important;
    letter-spacing: var(--md-sys-typescale-headline-large-tracking) !important;
    padding-top: 0 !important; /* supprime le padding-top par défaut de Streamlit */
}}
h2, h3 {{
    line-height: var(--md-sys-typescale-headline-small-line-height) !important;
    letter-spacing: var(--md-sys-typescale-headline-small-tracking) !important;
    padding-top: 0 !important; /* supprime le padding-top par défaut de Streamlit */
}}
hr {{
    margin: 1rem 0 !important; /* supprime le margin par défaut de Streamlit */
}}
[data-testid="stHeaderLogo"] {{
    margin-left: 110px !important;
}}

/* ── Ligne de titre + actions (st.title() + boutons) : padding-bottom ──
   ── pour espacer du contenu suivant, à poser sur un st.container()
*/
.st-key-ge-header-row {{
    margin-bottom: 1rem !important;
}}
.st-key-ge-header-row [class*="st-key-ge-btn-"] {{
    align-items: flex-end !important;
}}
"""

_LAYOUT_CSS = f"<style>{_LAYOUT_CSS_BODY}</style>"


def inject_ge_layout():
    st.html(_LAYOUT_CSS)


# Exposé pour combinaison dans styles.py — évite un st.markdown séparé
LAYOUT_CSS = _LAYOUT_CSS_BODY
