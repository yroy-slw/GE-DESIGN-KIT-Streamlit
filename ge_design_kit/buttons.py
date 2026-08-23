"""
ge_design_kit.buttons
------------------------
Styles CSS pour toutes les variantes de st.button/st.form_submit_button du kit

── Taxonomie des variantes ──────────────────────────────────────────

  FILLED_BUTTON_KEY_PREFIX    fond plein couleur primary, libellé (+
                               icône optionnelle) en on-primary — M3
                               "Filled Button", l'action principale d'un
                               écran (ex: "Télécharger en CSV")
  ICON_BUTTON_KEY_PREFIX      bouton rond, icône seule, fond plein
                               couleur primary (ex: bouton recherche rond)
  OUTLINED_BUTTON_KEY_PREFIX  contour fin, fond transparent
                               (ex: "Importer manuellement", "Comparer",
                               "Exporter")
  TEXT_BUTTON_KEY_PREFIX      pas de bordure ni de fond, juste le
                               libellé coloré (ex: "Annuler la sélection")
"""

import streamlit as st

FILLED_BUTTON_KEY_PREFIX = "ge-btn-filled-"
ICON_BUTTON_KEY_PREFIX = "ge-btn-icon-"
OUTLINED_BUTTON_KEY_PREFIX = "ge-btn-outlined-"
TEXT_BUTTON_KEY_PREFIX = "ge-btn-text-"

# Alias historique — conservé pour ne pas casser les imports existants
PILL_BUTTON_KEY_PREFIX = OUTLINED_BUTTON_KEY_PREFIX

BUTTONS_CSS = f"""
[class*="st-key-{FILLED_BUTTON_KEY_PREFIX}"] {{
    flex-shrink: 0 !important;
}}
[class*="st-key-{FILLED_BUTTON_KEY_PREFIX}"] button {{
    border-radius: var(--md-sys-shape-corner-full) !important;
    border: none !important;
    background: var(--md-sys-color-primary) !important;
    color: var(--md-sys-color-on-primary) !important;
    font-weight: var(--md-sys-typescale-label-medium-weight, 500) !important;
    padding: 10px 1rem !important;
    width: auto !important;
    min-width: 0 !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}}
[class*="st-key-{FILLED_BUTTON_KEY_PREFIX}"] button p {{
    white-space: nowrap !important;
}}
[class*="st-key-{FILLED_BUTTON_KEY_PREFIX}"] button:not(:disabled):hover {{
    background: color-mix(in srgb, var(--md-sys-color-primary) 92%, black) !important;
}}
[class*="st-key-{FILLED_BUTTON_KEY_PREFIX}"] button:disabled {{
    background: var(--md-sys-color-outline-variant) !important;
    color: var(--md-sys-color-on-surface-variant) !important;
    opacity: 0.6;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] {{
    flex-shrink: 0 !important;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] button {{
    border-radius: var(--md-sys-shape-corner-full) !important;
    background: var(--md-sys-color-primary) !important;
    border: none !important;
    width: 56px !important;
    height: 56px !important;
    padding: 0 !important;
    min-width: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] button * {{
    color: var(--md-sys-color-on-primary) !important;
    font-size: 1.5rem;
}}
[class*="st-key-{ICON_BUTTON_KEY_PREFIX}"] button:disabled {{
    background: var(--md-sys-color-outline-variant) !important;
    opacity: 0.6;
}}
[class*="st-key-{OUTLINED_BUTTON_KEY_PREFIX}"] {{
    flex-shrink: 0 !important;
}}
[class*="st-key-{OUTLINED_BUTTON_KEY_PREFIX}"] button {{
    border-radius: var(--md-sys-shape-corner-full) !important;
    border: 1px solid var(--md-sys-color-outline) !important;
    background: var(--md-sys-color-surface) !important;
    color: var(--md-sys-color-primary) !important;
    font-weight: 500 !important;
    padding: calc(var(--spacing) * 2) 1rem !important;
    width: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}}
[class*="st-key-{OUTLINED_BUTTON_KEY_PREFIX}"] button p {{
    white-space: nowrap !important;
}}
[class*="st-key-{OUTLINED_BUTTON_KEY_PREFIX}"] button:not(:disabled):hover {{
    border-color: var(--md-sys-color-primary) !important;
    background: color-mix(in srgb, var(--md-sys-color-primary) 6%, transparent) !important;
}}
[class*="st-key-{OUTLINED_BUTTON_KEY_PREFIX}"] button:disabled {{
    border-color: var(--md-sys-color-state-opacity-12, rgba(0, 51, 85, 0.12)) !important;
    color: var(--md-sys-color-on-surface-variant) !important;
    opacity: 0.6;
}}
[class*="st-key-{TEXT_BUTTON_KEY_PREFIX}"] {{
    flex-shrink: 0 !important;
}}
[class*="st-key-{TEXT_BUTTON_KEY_PREFIX}"] button {{
    border: none !important;
    background: transparent !important;
    color: var(--md-sys-color-primary) !important;
    font-weight: 500 !important;
    border-radius: var(--md-sys-shape-corner-full) !important;
    padding: calc(var(--spacing) * 2) 1rem !important;
    width: auto !important;
    flex-shrink: 0 !important;
    white-space: nowrap !important;
}}
[class*="st-key-{TEXT_BUTTON_KEY_PREFIX}"] button p {{
    white-space: nowrap !important;
}}
[class*="st-key-{TEXT_BUTTON_KEY_PREFIX}"] button:not(:disabled):hover {{
    background: color-mix(in srgb, var(--md-sys-color-primary) 6%, transparent) !important;
}}
[class*="st-key-{TEXT_BUTTON_KEY_PREFIX}"] button:disabled {{
    color: var(--md-sys-color-on-surface-variant) !important;
    opacity: 0.6;
}}

/*
   ── Barre de sélection (st.columns + st.button) : alignement horizontal ──
   ── et espacement entre boutons, pour les boutons de sélection de ──
   ── lignes du tableau (st.dataframe). Le contenu de cette barre est ──
   ── injecté après coup dans le slot réservé par st.empty() plus haut. ──
*/

.st-key-ge-selection-bar-row [data-testid="stHorizontalBlock"] {{
    justify-content: space-between !important;
}}
.st-key-ge-selection-bar-row [data-testid="stColumn"] {{
    flex: 0 1 auto !important;
    width: auto !important;
}}
.st-key-ge-button-group {{
    display: flex !important;
    flex-direction: row !important;
    gap: 1rem !important;
    align-items: center !important;
}}
"""


def ge_label_spacer(height_px: int = 10):
    """
    Espaceur invisible de la hauteur d'un label de widget Streamlit
    (10px par défaut, calibré visuellement). Utile pour aligner
    verticalement un bouton (st.button/st.form_submit_button, qui n'a
    pas de label au-dessus de lui) avec des champs voisins qui, eux,
    affichent un label (text_input, selectbox...) — sans ce spacer,
    le bouton apparaît plus haut que les champs à côté de lui.
    """
    st.html(f'<div style="height:{height_px}px;"></div>')