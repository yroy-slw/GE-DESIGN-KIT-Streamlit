"""
ge_design_kit.breadcrumb
--------------------------
Fil d'Ariane GE-DESIGN : "Accueil › Section › Page courante", toujours
juste au-dessus du h1 de contenu (pattern présent dans tous nos
wireframes SuisseVote / MemIA).

Streamlit n'a pas de composant natif équivalent, la seule option
"native" (st.page_link) impose son propre style, non personnalisable
finement. On construit donc ge_breadcrumb() sur le même pattern que
ge_sidebar() : liens cliquables (sauf le dernier, qui est la page
courante, non cliquable), séparateur chevron Material Symbols.

Le composant remonte l'id de l'item cliqué via st.session_state
(même pattern trigger que ge_sidebar), ensuite (st.switch_page, ou routing par état).
"""

import streamlit as st
from .icons import ICON_FONT_CSS

_ge_breadcrumb = st.components.v2.component(
    name="ge_breadcrumb",
    html="""<nav class="ge-breadcrumb" id="ge-breadcrumb" aria-label="Fil d'Ariane"></nav>""",
    css=ICON_FONT_CSS + """
    .ge-breadcrumb {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: calc(var(--spacing) * 1);
        font-family: var(--st-font, sans-serif);
        font-size: var(--md-sys-typescale-body-medium-size);
        line-height: var(--md-sys-typescale-body-medium-line-height);
        margin-bottom: calc(var(--spacing) * 3);
    }
    .ge-breadcrumb-item {
        color: var(--md-sys-color-on-surface-variant);
    }
    .ge-breadcrumb-item.link {
        color: var(--md-sys-color-primary);
        cursor: pointer;
    }
    .ge-breadcrumb-item.link:hover {
        text-decoration: underline;
    }
    .ge-breadcrumb-item.current {
        color: var(--md-sys-color-on-surface-variant);
        font-weight: 400;
    }
    .ge-breadcrumb-sep {
        font-size: 16px;
        color: var(--md-sys-color-on-surface-variant);
        opacity: 0.6;
        display: flex;
        align-items: center;
    }
    """,
    js="""
    export default function({ parentElement, data, setTriggerValue }) {
        const nav = parentElement.querySelector('#ge-breadcrumb');
        nav.innerHTML = '';

        const items = data.items || [];
        items.forEach((item, index) => {
            const isLast = index === items.length - 1;

            const el = document.createElement('span');
            el.textContent = item.label;

            if (isLast) {
                el.className = 'ge-breadcrumb-item current';
            } else {
                el.className = 'ge-breadcrumb-item link';
                el.onclick = () => setTriggerValue('selected', item.id);
            }
            nav.appendChild(el);

            if (!isLast) {
                const sep = document.createElement('span');
                sep.className = 'ge-breadcrumb-sep material-symbols-outlined';
                sep.textContent = 'chevron_right';
                nav.appendChild(sep);
            }
        });
    }
    """,
)


def ge_breadcrumb(items: list[dict], key: str = "ge_breadcrumb"):
    """
    Affiche un fil d'Ariane GE-DESIGN.

    items: liste ordonnée de dicts {id, label} — le DERNIER élément
    est automatiquement traité comme la page courante (non cliquable,
    couleur pleine) ; tous les précédents sont cliquables (couleur
    primary, soulignés au survol).

    Retourne l'id de l'item cliqué durant ce run (ou None).

    Exemple :
        clicked = ge_breadcrumb(
            items=[
                {"id": "home", "label": "Accueil"},
                {"id": "operations", "label": "Opérations"},
                {"id": "current", "label": "Votation fédérale du 17.06.2025"},
            ],
            key="page_breadcrumb",
        )
        if clicked:
            st.session_state.current_page = clicked
            st.rerun()
    """
    result = _ge_breadcrumb(key=key, data={"items": items}, on_selected_change=lambda: None)
    return result.selected
