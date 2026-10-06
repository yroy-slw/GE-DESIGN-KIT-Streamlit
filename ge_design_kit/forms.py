"""
ge_design_kit.forms
---------------------
Styles CSS pour les widgets Streamlit NATIFS (text_input, selectbox, toggle) — pas de composant CCv2 ici.
"""

# Dimensions du toggle (rail + curseur) — ajustables directement ici.
TOGGLE_TRACK_WIDTH_PX = 44
TOGGLE_TRACK_HEIGHT_PX = 24
TOGGLE_THUMB_SIZE_PX = 20
GE_TOGGLE_KEY_PREFIX = "ge-toggle-"
GE_CHEKBOX_KEY_PREFIX = "ge-checkbox-"

FORMS_CSS = f"""
[data-testid="stTextInputRootElement"] {{
    border-radius: var(--md-sys-shape-corner-extra-small) !important;
    border: 1px solid var(--md-sys-color-outline) !important;
    background: var(--md-sys-color-surface) !important;
    box-shadow: 0 1px 2px 0 rgba(18, 18, 23, 0.05) !important;
    height: 56px !important;
    padding: 0 calc(var(--spacing) * 3) !important;
    display: flex !important;
    align-items: center !important;
    align-self: stretch !important;
}}
[data-testid="stTextInputRootElement"] input[type="text"] {{
    background: transparent !important;
    border: none !important;
    height: 100% !important;
    font-size: 16px !important;
}}
[data-testid="stTextInputRootElement"]:focus-within {{
    border-color: var(--md-sys-color-primary) !important;
    box-shadow: 0 0 0 1px var(--md-sys-color-primary) !important;
}}

/* ── Selectbox (st.selectbox) : alignement vertical du champ + icône ──
*/
[data-testid="stSelectbox"] .react-aria-ComboBox [role="group"] {{
    border-radius: var(--md-sys-shape-corner-extra-small) !important;
    border: 1px solid var(--md-sys-color-outline) !important;
    background: var(--md-sys-color-surface) !important;
    box-shadow: 0 1px 2px 0 rgba(18, 18, 23, 0.05) !important;
    height: 56px !important;
    padding: 0 calc(var(--spacing) * 3) !important;
    display: flex !important;
    align-items: center !important;
    align-self: stretch !important;
}}
[data-testid="stSelectbox"] .react-aria-ComboBox [role="group"] input[role="combobox"] {{
    font-size: 16px !important;
}}

/* ── Toggle (st.checkbox) : rail + curseur, alignement vertical ── 
*/
[data-testid="stCheckbox"] label > div:first-of-type {{
    width: {TOGGLE_TRACK_WIDTH_PX}px !important;
    height: {TOGGLE_TRACK_HEIGHT_PX}px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 2px !important;
    box-sizing: border-box !important;
}}
[data-testid="stCheckbox"] label > div:first-of-type > div {{
    width: {TOGGLE_THUMB_SIZE_PX}px !important;
    height: {TOGGLE_THUMB_SIZE_PX}px !important;
    transform: none !important;
    margin-left: 0;
    transition: margin-left 0.15s ease;
}}
[data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type > div {{
    margin-left: auto !important;
}}
[data-testid="stCheckbox"] label {{
    align-items: center !important;
}}

[class*="st-key-{GE_CHEKBOX_KEY_PREFIX}"] label > div:first-of-type {{
    width: 20px !important;
    height: 20px !important;
}}

/* ── Alignement vertical d'une ligne de filtres (input/select/toggle) ──
   ── à poser sur un st.container(key="ge-filter-row") englobant la ligne. ── */
.st-key-ge-filter-row [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
}}

/* ── Formulaire de recherche (champ + bouton submit lié via Entrée) ──
   ── st.form ajoute par défaut une boîte/padding : on la neutralise ──
   ── pour ne garder que notre propre mise en page ── */
.st-key-ge-search-form {{
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}}
"""