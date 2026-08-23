"""
ge_design_kit.fonts
---------------------
Charge les polices externes (Roboto + Material Symbols) via Google
Fonts.
"""

import streamlit as st

FONT_IMPORT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100..900;1,100..900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');
"""


def inject_ge_fonts():
    """
    Pour minimiser le nombre de stElementContainer vides dans le DOM,
    préfèrer ge_design_kit.styles.inject_ge_styles()
    """
    st.html(f"<style>{FONT_IMPORT_CSS}</style>")
