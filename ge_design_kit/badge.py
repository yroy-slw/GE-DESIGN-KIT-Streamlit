"""
ge_design_kit.badge
---------------------
Badge/chip de statut GE-DESIGN (Figma "MD_Chips", node 233:6752 —
Material "Input chip"). Composant d'affichage pur, pas d'interaction :
pas de trigger, pas de valeur de retour.

Réutilisable seul (ex: statut dans une card, un détail de page) ou
comme brique interne d'un composant composite (cf. list.py, dont
chaque ligne affiche un badge) — dans ce 2ᵉ cas la variante
`.ge-badge` est réimplémentée par le composant hôte, PAS en appelant
ge_badge() depuis la boucle de rendu : un appel CCv2 (ge_badge()) monte
TOUJOURS son propre custom element top-niveau, il ne peut pas être
imbriqué dans le DOM d'un autre composant CCv2 (cf. icons.py pour le
même sujet — CSS dupliquée entre fichiers, Shadow DOM isolé par
composant).
"""

import streamlit as st

# Exposé pour réutilisation par list.py (et tout futur composant
# composite ayant besoin du même badge) — évite de laisser diverger
# deux copies de la même règle de style.
BADGE_CSS = """
.ge-badge {
    display: inline-flex;
    align-items: center;
    gap: calc(var(--spacing) * 1);
    padding: 4px 8px;
    border-radius: var(--md-sys-shape-corner-extra-small);
    font-family: var(--st-font, sans-serif);
    font-size: var(--md-sys-typescale-body-small-size);
    line-height: var(--md-sys-typescale-body-small-line-height);
    letter-spacing: var(--md-sys-typescale-body-small-tracking);
    white-space: nowrap;
}
.ge-badge.neutral {
    background: var(--md-sys-color-secondary-container);
    color: var(--md-sys-color-on-secondary-container);
}
.ge-badge.success {
    background: var(--md-sys-color-success-container);
    color: var(--md-sys-color-on-success-container);
}
.ge-badge.warning {
    background: var(--md-sys-color-warning-container);
    color: var(--md-sys-color-on-warning-container);
}
.ge-badge.error {
    background: var(--md-sys-color-error-container);
    color: var(--md-sys-color-on-error-container);
}
"""

_ge_badge = st.components.v2.component(
    name="ge_badge",
    html="""<span class="ge-badge" id="ge-badge"></span>""",
    css=BADGE_CSS,
    js="""
    export default function({ parentElement, data }) {
        const el = parentElement.querySelector('#ge-badge');
        el.className = 'ge-badge ' + (data.variant || 'neutral');
        el.textContent = data.label || '';
    }
    """,
)


def ge_badge(label: str, variant: str = "neutral", key: str = "ge_badge"):
    """
    Affiche un badge/chip de statut GE-DESIGN. Composant d'affichage
    pur (pas de retour, pas d'interaction).

    variant: "neutral" (défaut, ex: "Non démarrée"), "success"
    (ex: "Analysée"), "warning" (ex: "En cours"), "error".

    Exemple :
        ge_badge("Non démarrée", key="badge_statut")
    """
    _ge_badge(key=key, data={"label": label, "variant": variant})
