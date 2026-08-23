"""
ge_design_kit.alerts
------------------------
Style CSS pour st.info/st.success/st.warning/st.error - widgets NATIFS
Streamlit (pas de CCv2 ici, comme dialog.py/forms.py), habillés pour
matcher GE-DESIGN "MD_Stacked card_info",
variant Type=Info — mêmes coins/ombre/typo pour les 3 autres variants,
juste la couleur de fond qui change selon le kind).

── Anatomie du DOM natif ──────────
  [data-testid="stAlert"]
    └── [data-testid="stAlertContainer"]        fond/coins/ombre à
          │                                     restyler ICI
          └── [data-testid="stAlertContentInfo"       <- un seul de ces
              |  data-testid="stAlertContentSuccess"     4 selon le kind
              |  data-testid="stAlertContentWarning"     (info/success/
              |  data-testid="stAlertContentError"]      warning/error)
                ├── [data-testid="stAlertTitle"]  titre optionnel — SEULEMENT
                │     └── ...> p                  si title=... est passé
                └── [data-testid="stMarkdownContainer"] > p   corps
"""

ALERTS_CSS = """
[data-testid="stAlertContainer"] {
    border-radius: var(--md-sys-shape-corner-medium) !important;
    box-shadow:
        0 1px 2px 0 rgba(24, 31, 37, 0.30),
        0 1px 6px 2px rgba(24, 31, 37, 0.15) !important;
}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"]) {
    background: var(--md-sys-color-primary-container) !important;
}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) {
    background: var(--md-sys-color-success-container) !important;
}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {
    background: var(--md-sys-color-warning-container) !important;
}
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {
    background: var(--md-sys-color-error-container) !important;
}
[data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] p {
    color: var(--md-sys-color-on-surface) !important;
    font-family: var(--md-sys-typescale-body-large-font) !important;
    font-size: var(--md-sys-typescale-body-large-size) !important;
    font-weight: var(--md-sys-typescale-body-large-weight) !important;
    line-height: var(--md-sys-typescale-body-large-line-height) !important;
    letter-spacing: var(--md-sys-typescale-body-large-tracking) !important;
}
[data-testid="stAlertTitle"] [data-testid="stMarkdownContainer"] p {
    font-family: var(--md-sys-typescale-label-large-font) !important;
    font-size: var(--md-sys-typescale-label-large-size) !important;
    font-weight: var(--md-sys-typescale-label-large-weight) !important;
    line-height: var(--md-sys-typescale-label-large-line-height) !important;
    letter-spacing: var(--md-sys-typescale-label-large-tracking) !important;
}
"""
