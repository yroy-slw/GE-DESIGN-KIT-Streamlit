"""
ge_design_kit.kpi
------------------
KPI card (chiffre + libellé), pattern repris de SuisseVote/MemIA.
Composant purement d'affichage (pas d'interaction retour vers Python).
"""

import streamlit as st

_ge_kpi = st.components.v2.component(
    name="ge_kpi",
    html="""<div class="ge-kpi"><div class="ge-kpi-num" id="ge-kpi-num"></div><div class="ge-kpi-lbl" id="ge-kpi-lbl"></div></div>""",
    css="""
    .ge-kpi {
        background: var(--md-sys-color-surface-container-highest, var(--st-secondary-background-color));
        border-radius: var(--md-sys-shape-corner-medium, var(--st-base-radius));
        padding: 0.5rem 1rem;
        font-family: var(--st-font);
    }
    .ge-kpi-num {
        font-size: 22px;
        font-weight: 600;
        color: var(--md-sys-color-on-surface);
        line-height: 1;
    }
    .ge-kpi-lbl {
        font-size: var(--md-sys-typescale-label-medium-size, 0.8em);
        color: var(--md-sys-color-on-surface-variant);
        margin-top: 0;
    }
    """,
    js="""
    export default function({ parentElement, data }) {
        parentElement.querySelector('#ge-kpi-num').textContent = data.value;
        parentElement.querySelector('#ge-kpi-lbl').textContent = data.label;
    }
    """,
)


def ge_kpi(value, label: str, key: str):
    """Affiche une KPI card simple (chiffre + libellé)."""
    _ge_kpi(key=key, data={"value": value, "label": label})
