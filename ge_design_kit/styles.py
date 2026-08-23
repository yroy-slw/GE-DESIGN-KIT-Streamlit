"""
ge_design_kit.styles
----------------------
Combine fonts + tokens + layout en UN SEUL appel.
appels séparés (inject_ge_fonts / inject_ge_tokens / inject_ge_layout).
"""

import streamlit as st

from .fonts import FONT_IMPORT_CSS
from .tokens import TOKENS_CSS
from .layout import LAYOUT_CSS
from .surface import SURFACE_CSS
from .forms import FORMS_CSS
from .buttons import BUTTONS_CSS
from .dialog import DIALOG_CSS
from .alerts import ALERTS_CSS


def inject_ge_styles():
    """
    A appeler UNE SEULE FOIS, tout en haut de app.py — remplace les
    3 appels inject_ge_fonts() + inject_ge_tokens() + inject_ge_layout().
    """
    combined = f"<style>{FONT_IMPORT_CSS}{TOKENS_CSS}{LAYOUT_CSS}{SURFACE_CSS}{FORMS_CSS}{BUTTONS_CSS}{DIALOG_CSS}{ALERTS_CSS}</style>"
    st.html(combined)
