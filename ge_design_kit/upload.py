"""
ge_design_kit.upload
----------------------
Bloc d'accroche pour l'import de fichiers — utilisé pour l'état VIDE
d'une page où l'utilisateur doit importer des données avant de voir un contenu.
"""

import streamlit as st

from .buttons import FILLED_BUTTON_KEY_PREFIX

UPLOAD_DROPZONE_KEY_PREFIX = "ge-upload-dropzone-"
# Conteneur dédié à l'icône du haut, séparé du bouton : sans lui, un
UPLOAD_ICON_KEY_PREFIX = "ge-upload-dropzone-icon-"

UPLOAD_CSS = f"""
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] {{
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(var(--spacing) * 4);
    padding: calc(var(--spacing) * 8) 0;
    width: 100%;
    text-align: center;
}}
/* Chaque enfant (icône/texte/séparateur en stElementContainer direct,
   bouton en stLayoutWrapper car passé par st.container()) est en
   width:100% par défaut — align-items du flex parent ne centre alors
   QUE la boîte, pas son contenu. text-align centre le texte/icône
   inline ; ces deux règles centrent le bouton (bloc, pas inline). */
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] [data-testid="stElementContainer"],
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] [data-testid="stLayoutWrapper"] {{
    display: flex;
    justify-content: center;
}}
/* Le stVerticalBlock du bouton (st.container(key=...)) a lui-même
   flex:1 par défaut (flex-basis compris, pas juste flex-grow) : il
   remplit tout le stLayoutWrapper ci-dessus et justify-content n'a
   alors plus rien à centrer. "flex:none" (pas juste flex-grow:0)
   annule aussi le flex-basis, sans quoi il garde sa largeur héritée
   même une fois flex-grow neutralisé. */
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] [data-testid="stVerticalBlock"],
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] [data-testid="stLayoutWrapper"] {{
    flex: none !important;
    width: auto !important;
    padding: 0 !important;
}}
/* Le composant icône Streamlit fixe font-size ET width/height (boîte
   carrée qui CLIPPE le glyphe) via une classe emotion générée — ne
   changer que font-size laisse le glyphe coincé dans son ancienne
   boîte, d'où les deux à surcharger ensemble. */
[class*="st-key-{UPLOAD_ICON_KEY_PREFIX}"] span {{
    font-size: 35px !important;
    width: 35px !important;
    height: 35px !important;
    color: var(--md-sys-color-on-surface) !important;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-title {{
    text-align: center;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-title p {{
    margin: 0;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-title p:first-child {{
    color: var(--md-sys-color-on-surface);
    font-size: var(--md-sys-typescale-label-large-size, 16px);
    font-weight: 500;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-title p:last-child {{
    color: var(--md-sys-color-on-surface-variant);
    font-size: var(--md-sys-typescale-body-small-size, 12px);
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-divider {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: calc(var(--spacing) * 4);
    width: 100%;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-divider span {{
    flex: 1 0 0;
    height: 1px;
    background: var(--md-sys-color-outline-variant);
    max-width: 134px;
}}
[class*="st-key-{UPLOAD_DROPZONE_KEY_PREFIX}"] .ge-upload-divider p {{
    color: var(--md-sys-color-on-surface);
    font-size: var(--md-sys-typescale-body-large-size, 16px);
    margin: 0;
    flex-shrink: 0;
}}
"""


def ge_upload_dropzone(
    icon: str,
    title: str,
    subtitle: str,
    button_label: str,
    button_icon: str = "",
    key: str = "ge_upload_dropzone",
) -> bool:
    """
    Icône + titre + sous-titre + séparateur "ou" + bouton (filled).

    `icon`/`button_icon` : nom Material Symbols SANS les ":material/ :"
    (ex: "upload_file"), même convention que partout ailleurs dans le
    kit — cf. fonts.google.com/icons.

    Retourne True si le bouton a été cliqué durant CE run (même
    convention que ge_card).
    """
    with st.container(key=f"{UPLOAD_DROPZONE_KEY_PREFIX}{key}"):
        with st.container(key=f"{UPLOAD_ICON_KEY_PREFIX}{key}"):
            st.markdown(f":material/{icon}:")
        st.html(f'<div class="ge-upload-title"><p>{title}</p><p>{subtitle}</p></div>')
        st.html('<div class="ge-upload-divider"><span></span><p>ou</p><span></span></div>')
        with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}{key}"):
            clicked = st.button(
                button_label,
                icon=f":material/{button_icon}:" if button_icon else None,
                key=f"btn_{key}",
            )
    return clicked
