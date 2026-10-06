import streamlit as st

from ge_design_kit import inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar, ge_sidebar

from debug_utils import (
    is_debug_enabled,
    log_session_state,
    render_debug_panel,
    render_debug_console_page,
)

if st.query_params.get("debug_console") == "1":
    if is_debug_enabled():
        render_debug_console_page()
    else:
        st.error("Mode debug non activé sur cette session.")
    st.stop()

st.set_page_config(page_title="MemIA — POC GE-DESIGN", layout="wide")

# ── Mode rail de la sidebar (icônes seules, cf. ge_sidebar/layout.py) ──
# — PAS le collapse natif de st.sidebar (montré/caché en entier
# uniquement, aucun mode intermédiaire). Basculé par le burger de
# ge_topbar via _toggle_sidebar plus bas. ──
if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False


def _toggle_sidebar():
    st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed


# ── Polices + tokens + layout GE-DESIGN ──
inject_ge_styles(sidebar_collapsed=st.session_state.sidebar_collapsed)

# ── Bandeau GE plein-largeur, au-dessus de tout ──
# Wrappé dans un container à clé fixe pour que layout.py puisse
# collapser proprement son slot de flux.
with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="MEMIA", user_label="Mon compte", env="DEV", on_toggle=_toggle_sidebar)

# ── État partagé entre TOUTES les pages — st.session_state survit à
# st.switch_page() (même session, script différent), contrairement à
# une simple variable Python locale. C'est le mécanisme qui permet à
# views/comparaison.py et views/export.py de savoir quelles opérations
# ont été sélectionnées sur views/operations.py (cf. data.py pour le
# détail: on stocke des id stables, pas les lignes elles-mêmes). ──
if "selected_operation_ids" not in st.session_state:
    st.session_state.selected_operation_ids = []


def _placeholder(title: str):
    """Fabrique une page minimale "à venir" pour les sections du menu
    pas encore construites — évite d'avoir un fichier quasi-vide par
    section tant qu'elles n'ont pas de vrai contenu."""
    def _render():
        st.title(title)
        st.info("Cette section n'est pas encore implémentée.")
    return _render


# ── Déclaration des pages réelles (st.navigation) — remplace l'ancien
# pattern session_state.current_page + rerun manuel (single-script).
# position="hidden": on garde ge_sidebar comme SEULE UI de navigation
# visible; st.navigation ne gère que le routing + la persistance de
# session_state en coulisses, son propre sélecteur de pages natif
# n'est jamais affiché. ──
page_operation = st.Page("views/operations.py", title="Opération", url_path="operation", default=True)
page_configuration = st.Page(_placeholder("Configuration"), title="Configuration", url_path="configuration")
page_interpretation = st.Page(_placeholder("Interprétation"), title="Interprétation", url_path="interpretation")
page_analyse = st.Page(_placeholder("Analyse"), title="Analyse", url_path="analyse")
page_verification = st.Page(_placeholder("Vérification"), title="Vérification", url_path="verification")
page_recherche = st.Page(_placeholder("Recherche"), title="Recherche", url_path="recherche")
# Comparer/Exporter: PAS dans ge_sidebar, atteintes uniquement via
# les boutons de la page Opération, une fois des lignes sélectionnées.
page_comparaison = st.Page("views/comparaison.py", title="Comparer", url_path="comparaison")
page_export = st.Page("views/export.py", title="Exporter", url_path="export")

pages = st.navigation(
    [
        page_operation, page_configuration, page_interpretation,
        page_analyse, page_verification, page_recherche,
        page_comparaison, page_export,
    ],
    position="hidden",
)

# Items visibles dans ge_sidebar — sous-ensemble des pages déclarées
# ci-dessus (pas Comparer/Exporter, cf. commentaire plus haut).
SIDEBAR_ID_TO_PAGE = {
    "operation": page_operation,
    "configuration": page_configuration,
    "interpretation": page_interpretation,
    "analyse": page_analyse,
    "verification": page_verification,
    "recherche": page_recherche,
}

# ── Sidebar native (position fixe, toujours "expanded" côté Streamlit —
# cf. _toggle_sidebar plus haut) + composant à l'intérieur ──
with st.sidebar:
    selected = ge_sidebar(
        items=[
            {"id": "operation", "label": "Opération", "icon": "add_circle"},
            {"id": "configuration", "label": "Configuration", "icon": "settings"},
            {"id": "interpretation", "label": "Interprétation", "icon": "assignment", "has_children": True},
            {"id": "analyse", "label": "Analyse", "icon": "scatter_plot", "has_children": True},
            {"id": "verification", "label": "Vérification", "icon": "verified_user", "has_children": True},
            {"id": "recherche", "label": "Recherche", "icon": "search"},
        ],
        # pages.url_path renvoie "" pour la page par défaut (Opération)
        # plutôt que "operation" d'où le repli explicite.
        active_id=pages.url_path or "operation",
        collapsed=st.session_state.sidebar_collapsed,
        key="main_sidebar",
    )
    if selected:
        st.switch_page(SIDEBAR_ID_TO_PAGE[selected])

log_session_state("app.py")
render_debug_panel()

pages.run()
