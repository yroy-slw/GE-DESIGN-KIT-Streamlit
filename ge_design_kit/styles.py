"""
ge_design_kit.styles
----------------------
Combine fonts + tokens + layout en UN SEUL appel.
appels séparés (inject_ge_fonts / inject_ge_tokens / inject_ge_layout).
"""

import streamlit as st

from .fonts import FONT_IMPORT_CSS
from .tokens import TOKENS_CSS
from .layout import get_layout_css
from .surface import SURFACE_CSS
from .forms import FORMS_CSS
from .buttons import BUTTONS_CSS
from .dialog import DIALOG_CSS
from .alerts import ALERTS_CSS
from .upload import UPLOAD_CSS


def inject_ge_styles(sidebar_collapsed: bool = False):
    """
    A appeler UNE SEULE FOIS, tout en haut de app.py — remplace les
    3 appels inject_ge_fonts() + inject_ge_tokens() + inject_ge_layout().

    sidebar_collapsed: doit matcher st.session_state.sidebar_collapsed
    (mode rail de la sidebar, cf. layout.py/sidebar.py/topbar.py).
    """
    layout_css = get_layout_css(sidebar_collapsed)
    combined = f"<style>{FONT_IMPORT_CSS}{TOKENS_CSS}{layout_css}{SURFACE_CSS}{FORMS_CSS}{BUTTONS_CSS}{DIALOG_CSS}{ALERTS_CSS}{UPLOAD_CSS}</style>"
    st.html(combined)
