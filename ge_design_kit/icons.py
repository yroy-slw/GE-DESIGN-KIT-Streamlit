"""
ge_design_kit.icons
---------------------
POINT D'ARCHITECTURE IMPORTANT — Shadow DOM et partage de CSS

Les composants Custom Components v2 sont rendus dans un Shadow DOM
isolé (voir sidebar.py, card.py...). Deux types de choses traversent
cette frontière depuis le document principal :
  - Les polices (ressources navigateur globales, comme des fichiers)
  - Les CSS Custom Properties héritées (--md-sys-color-*, --spacing...)

Mais pas :
  - Les règles CSS classiques (`.material-symbols-outlined { ... }`)
"""

ICON_FONT_CSS = """
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-weight: normal;
    font-style: normal;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    vertical-align: middle;
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}
"""
