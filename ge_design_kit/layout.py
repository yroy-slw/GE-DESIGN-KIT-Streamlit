"""
ge_design_kit.layout
----------------------
Neutralise les contraintes de layout par défaut de Streamlit
(conteneur centré avec max-width) et restyle le st.sidebar
natif aux couleurs GE-DESIGN — plutôt que de simuler une sidebar
avec st.columns.

La largeur de la sidebar dépend de `sidebar_collapsed` (mode rail
d'icônes seules, Figma node 525:53468, vs mode normal icône+libellé,
node 558:2156) — PAS du collapse natif de st.sidebar, qui ne sait que
montrer/cacher en entier, pas un mode rail à largeur intermédiaire.
Ce flag vient de st.session_state (basculé par le burger de
ge_topbar, cf. app.py) et doit être assorti à ge_sidebar(collapsed=...).
"""

import streamlit as st
from .topbar import TOPBAR_HEIGHT_PX

# Clé utilisée pour wrapper l'appel à ge_topbar() dans app.py — doit
# matcher exactement st.container(key=TOPBAR_SLOT_KEY) côté app.py.
TOPBAR_SLOT_KEY = "ge_topbar_slot"

# Largeurs de section[data-testid="stSidebar"] — Figma CHA_nav: 280px
# déplié (node 558:2156) / 91px rail (node 525:53468).
_SIDEBAR_WIDTH_EXPANDED_PX = 280
_SIDEBAR_WIDTH_COLLAPSED_PX = 91


def _layout_css_body(sidebar_collapsed: bool = False) -> str:
    sidebar_width_px = _SIDEBAR_WIDTH_COLLAPSED_PX if sidebar_collapsed else _SIDEBAR_WIDTH_EXPANDED_PX
    return f"""
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

/* ── Sidebar native : restyle GE-DESIGN + décalée sous notre topbar. ──
   ── Largeur dynamique (cf. docstring du module) : ge_sidebar() doit ──
   ── recevoir le MÊME sidebar_collapsed pour basculer en mode rail. ── */
section[data-testid="stSidebar"] {{
    background: var(--md-sys-color-surface-container-low);
    border-right: 1px solid var(--md-sys-color-outline-variant);
    width: {sidebar_width_px}px !important;
    /* Streamlit (sidebar redimensionnable à la souris) impose ses
       propres min-width:200px/max-width:600px via une classe interne
       (.st-emotion-cache-*) — sans ces deux overrides, le navigateur
       écrête notre width:91px (mode rail) à 200px, le min-width
       gagnant TOUJOURS sur width quel que soit !important. On verrouille
       aussi la largeur exacte dans les deux modes : plus de
       redimensionnement manuel par l'utilisateur, cohérent avec le
       comportement déjà en place avant le mode rail (width forcé à
       260px, jamais remis en question jusqu'ici simplement parce que
       260 tombait DANS la plage [200,600] autorisée par Streamlit). */
    min-width: {sidebar_width_px}px !important;
    max-width: {sidebar_width_px}px !important;
    top: {TOPBAR_HEIGHT_PX}px !important;
    height: calc(100vh - {TOPBAR_HEIGHT_PX}px) !important;
    transition: width 0.15s ease;
}}
section[data-testid="stSidebar"] > div {{
    padding-top: 0;
}}

/* ── Header natif de la sidebar (son propre logo + sa propre flèche ──
   ── de collapse) : complètement supprimé, redondant avec notre ──
   ── burger/marque dans ge_topbar (qui pilote le mode rail/normal de ──
   ── façon cohérente dans les deux états, cf. topbar.py). display: ──
   ── none referme aussi l'espace qu'il réservait en haut de la ──
   ── sidebar — ge_sidebar() démarre directement sous son propre ──
   ── padding interne. ── */
[data-testid="stSidebarHeader"] {{
    display: none !important;
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

/* ── Styles CSS pour la gallery de composants ── */
.st-key-wrapper_gallery_container {{
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 1rem;
}}

.st-key-wrapper_gallery_container  div:has(div.st-key-stepper_gallery_container) {{
    position: sticky;
    top: {TOPBAR_HEIGHT_PX}px
}}

.st-key-main_gallery_container {{
    max-width: 80% !important;
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

/* ── Ligne de titre + actions (st.title() + boutons, cf. Figma node ──
   ── 529:58860 : titre + bouton "Importer manuellement" sur la MÊME ──
   ── ligne) — st.container(key="ge-header-row") + st.columns([5, 2]) ──
   ── (cf. views/operations.py). Sans cette règle, le bouton de la ──
   ── dernière colonne reste collé au bord GAUCHE de sa colonne (large ──
   ── de 2/7 de la ligne), visuellement loin du bord droit réel de la ──
   ── page — flex + justify-content:flex-end le pousse jusqu'au bord ──
   ── droit de SA colonne, qui lui coïncide avec le bord droit de la ──
   ── page entière (c'est la dernière). ── */
.st-key-ge-header-row {{
    margin-bottom: 1rem !important;
}}
.st-key-ge-header-row [data-testid="stColumn"]:last-child {{
    display: flex;
    justify-content: flex-end;
}}
.st-key-ge-header-row [class*="st-key-ge-btn-"] {{
    align-items: flex-end !important;
}}
"""


def inject_ge_layout(sidebar_collapsed: bool = False):
    st.html(f"<style>{_layout_css_body(sidebar_collapsed)}</style>")


def get_layout_css(sidebar_collapsed: bool = False) -> str:
    """Exposé pour combinaison dans styles.py — évite un st.html() séparé."""
    return _layout_css_body(sidebar_collapsed)
