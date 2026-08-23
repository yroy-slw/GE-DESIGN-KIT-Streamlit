"""
ge_design_kit.forms
---------------------
Styles CSS pour les widgets Streamlit NATIFS (text_input, selectbox,
checkbox, toggle) — pas de composant CCv2 ici.

── Checkbox vs Toggle ────────────────────────────────────────────────
st.checkbox et st.toggle sont un SEUL ET MÊME composant côté Streamlit :
même wrapper, même `data-testid="stCheckbox"`. Seule leur structure DOM
interne diffère une fois coché.
"""

# Dimensions de la case à cocher standard.
CHECKBOX_SIZE_PX = 18

# Dimensions du toggle (rail + curseur) — ajustables directement ici.
TOGGLE_TRACK_WIDTH_PX = 44
TOGGLE_TRACK_HEIGHT_PX = 24
TOGGLE_THUMB_SIZE_PX = 20

# À poser sur un st.container(key=f"{GE_TOGGLE_KEY_PREFIX}mon_toggle")
# englobant l'appel à st.toggle — cf. docstring du module.
GE_TOGGLE_KEY_PREFIX = "ge-toggle-"

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

/* ── Checkbox standard (st.checkbox) : case à cocher, style par défaut ──
   ── de [data-testid="stCheckbox"] - s'applique à TOUT st.checkbox/ ──
   ── st.toggle non enveloppé dans le conteneur GE_TOGGLE_KEY_PREFIX. ──
   ── Valeurs (couleur bordure, radius 2px) reprises telles quelles du ──*/
[data-testid="stCheckbox"] label > div:first-of-type {{
    width: {CHECKBOX_SIZE_PX}px !important;
    height: {CHECKBOX_SIZE_PX}px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border-radius: 2px !important;
    border: 2px solid var(--md-sys-color-on-surface-variant) !important;
    background: var(--md-sys-color-surface) !important;
    box-sizing: border-box !important;
    transition: background 0.12s, border-color 0.12s;
}}
[data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type {{
    background: var(--md-sys-color-primary) !important;
    border-color: var(--md-sys-color-primary) !important;
}}
[data-testid="stCheckbox"] label > div:first-of-type svg {{
    /* Streamlit fixe cette icône (un polyline SVG, pas de path) à 14px
       inline — sans !important ici notre 100% ne l'emporte jamais, la
       coche reste petite/fine au lieu de remplir la case. Le
       stroke-width de la coche est défini en unités du viewBox (10x8) :
       agrandir le SVG l'épaissit proportionnellement, donc ce seul fix
       corrige aussi son épaisseur trop fine par rapport à la maquette
       Figma. */
    width: 100% !important;
    height: 100% !important;
    color: var(--md-sys-color-on-primary, white) !important;
}}
[data-testid="stCheckbox"] label {{
    align-items: center !important;
}}
[data-testid="stCheckbox"] label[data-disabled="true"] > div:first-of-type {{
    opacity: 0.6 !important;
}}
[data-testid="stCheckbox"] label[data-disabled="true"][data-selected="true"] > div:first-of-type {{
    background: var(--md-sys-color-outline-variant) !important;
    border-color: var(--md-sys-color-outline-variant) !important;
}}
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label > div:first-of-type {{
    width: {TOGGLE_TRACK_WIDTH_PX}px !important;
    height: {TOGGLE_TRACK_HEIGHT_PX}px !important;
    border-radius: {TOGGLE_TRACK_HEIGHT_PX}px !important;
    border: none !important;
    background: var(--md-sys-color-outline) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    padding: 0 2px !important;
    box-sizing: border-box !important;
}}
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type {{
    background: var(--md-sys-color-primary) !important;
    border-color: var(--md-sys-color-primary) !important;
}}
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label > div:first-of-type > div {{
    width: {TOGGLE_THUMB_SIZE_PX}px !important;
    height: {TOGGLE_THUMB_SIZE_PX}px !important;
    border-radius: 999px !important;
    background: var(--md-sys-color-surface) !important;
    transform: none !important;
    margin-left: 0;
    transition: margin-left 0.15s ease;
}}
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label[data-selected="true"] > div:first-of-type > div {{
    margin-left: auto !important;
}}
/* ── Toggle désactivé : même logique que le checkbox ci-dessus. ── */
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label[data-disabled="true"] > div:first-of-type {{
    opacity: 0.6 !important;
}}
[class*="st-key-{GE_TOGGLE_KEY_PREFIX}"] [data-testid="stCheckbox"] label[data-disabled="true"][data-selected="true"] > div:first-of-type {{
    background: var(--md-sys-color-outline-variant) !important;
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