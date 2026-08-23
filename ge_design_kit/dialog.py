"""
ge_design_kit.dialog
------------------------
Style CSS pour st.dialog() - le modal NATIF de Streamlit

st.dialog() est un DÉCORATEUR: on écrit une fonction, on l'appelle
depuis un handler de clic (ex: `if st.button(...): my_dialog()`), et
Streamlit affiche son contenu dans l'overlay. Voir la docstring de
`st.dialog` (module streamlit) pour la doc complète, un seul dialog
peut être ouvert à la fois.

── Anatomie du DOM natif (Streamlit 1.62) ──────────
  [data-testid="stDialog"]     scrim plein écran (position:fixed, centre
    │                          le panneau, gère le clic-en-dehors)
    └── div                    panneau visible — fond/coins/ombre à
          │                    restyler pour matcher GE-DESIGN
          ├── div                 zone invisible de fermeture au clic-dehors
          ├── section              layout du contenu, pas de style propre
          │     ├── button[aria-label="Close"]   croix de fermeture
          │     │                  (native — ESC / clic-dehors / clic croix
          │     │                  gérés par Streamlit lui-même)
          │     ├── h2              titre (texte passé à @st.dialog("..."))
          │     └── div > [data-testid="stVerticalBlock"]  corps du
          │                        dialog (contenu de la fonction décorée)
"""

DIALOG_CSS = """
[data-testid="stDialog"] {
    background: var(--md-sys-color-scrim) !important;
}
[data-testid="stDialog"] > div {
    border-radius: var(--md-sys-shape-corner-extra-small) !important;
    background: var(--md-sys-color-surface) !important;
    box-shadow:
        0 1px 2px 0 rgba(24, 31, 37, 0.08),
        0 1px 3px 1px rgba(24, 31, 37, 0.15) !important;
}
[data-testid="stDialog"] h2 {
    font-family: var(--md-sys-typescale-label-large-font) !important;
    font-size: var(--md-sys-typescale-label-large-size) !important;
    font-weight: var(--md-sys-typescale-label-large-weight) !important;
    line-height: var(--md-sys-typescale-label-large-line-height) !important;
    letter-spacing: var(--md-sys-typescale-label-large-tracking) !important;
    color: var(--md-sys-color-on-surface) !important;
    padding: 24px 24px 12px !important;
}
[data-testid="stDialog"] button[aria-label="Close"] svg {
    color: var(--md-sys-color-on-surface) !important;
}
[data-testid="stDialog"] button[aria-label="Close"]:hover {
    background: var(--md-sys-color-state-opacity-8, rgba(0, 51, 85, 0.08)) !important;
}
"""
