"""
ge_design_kit.surface
------------------------
Conteneurs de page GE-DESIGN — DIFFÉRENT de ge_card : ge_surface est
un vrai st.container() natif qui peut CONTENIR n'importe quel widget
Streamlit (colonnes, tableaux, filtres, nos ge_kpi/ge_card...), alors
que ge_card est un composant CCv2 figé (titre + texte + un bouton),
incapable de contenir d'autres widgets Streamlit à l'intérieur de son
Shadow DOM.

Pour ajouter un nouveau variant plus tard : ajouter une entrée dans
SURFACE_VARIANTS avec ses propriétés CSS, rien d'autre à toucher.
"""

import streamlit as st

# Un préfixe de clé dédié par variant — chacun devient son propre
# sélecteur CSS, indépendant des autres.
SURFACE_VARIANTS = {
    # Carte de page principale : fond blanc, ombre elevation-1.
    # (les valeurs rgba viennent de Figma
    "card": {
        "key_prefix": "ge-surface-card-",
        "css": """
            border-radius: var(--md-sys-shape-corner-medium);
            background: var(--md-sys-color-surface);
            box-shadow:
                0 1px 2px 0 rgba(24, 31, 37, 0.08),
                0 1px 3px 1px rgba(24, 31, 37, 0.15);
            padding: calc(var(--spacing) * 6);
        """,
    },
    # Bloc "inset" : fond légèrement teinté, pas d'ombre. Utilisé pour
    # sous-grouper du contenu à l'intérieur d'une carte "card" (ex: la
    # rangée de KPI cards).
    "inset": {
        "key_prefix": "ge-surface-inset-",
        "css": """
            border-radius: var(--md-sys-shape-corner-medium);
            background: var(--md-sys-color-surface-bright);
            padding: calc(var(--spacing) * 4) calc(var(--spacing) * 6);
            gap: 0.5rem;
        """,
    },
}

# Génère une règle CSS par variant, toutes combinées en une seule
# constante à intégrer dans l'injection globale (cf. styles.py).
SURFACE_CSS = "\n".join(
    f'[class*="st-key-{v["key_prefix"]}"] {{{v["css"]}}}'
    for v in SURFACE_VARIANTS.values()
)


def ge_surface(key: str, variant: str = "card"):
    """
    Conteneur de page GE-DESIGN. S'utilise comme un st.container()
    normal, peut contenir n'importe quel widget Streamlit, y compris
    nos composants ge_kpi/ge_card/etc.

    `key` est un identifiant COURT et unique pour CETTE surface sur la
    page (ex: "operations", "kpi-row"), le préfixe du variant est
    ajouté automatiquement, pas besoin de le répéter.

    `variant` : "card" (défaut, fond blanc + ombre) ou "inset" (fond
    teinté, sans ombre, pour sous-grouper du contenu dans une carte).

    Exemple :
        with ge_surface("operations"):          # variant="card"
            st.subheader("Choisir la votation à analyser")
            with ge_surface("kpi-row", variant="inset"):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    ge_kpi(4, "Opérations disponibles", key="kpi_total")
                ...
    """
    if variant not in SURFACE_VARIANTS:
        raise ValueError(f"Variant inconnu : {variant!r}. Choix possibles : {list(SURFACE_VARIANTS)}")
    prefix = SURFACE_VARIANTS[variant]["key_prefix"]
    return st.container(key=f"{prefix}{key}")
