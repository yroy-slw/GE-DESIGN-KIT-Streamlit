"""
ge_design_kit.list
---------------------
Liste cliquable GE-DESIGN (Figma "MD_List item transverse", node
529:60163 — ex: "Sélectionner un groupe de scrutins"). Lignes pleine
largeur (100% du parent), séparées par un divider, chacune avec un
badge de statut (cf. badge.py) et une flèche de navigation à droite.

Même pattern que ge_sidebar()/ge_breadcrumb() : un appel = toute la
liste, items passés en Python (liste de dicts), clic remonté via
trigger CCv2 → id de l'item cliqué (ou None). Le badge de chaque ligne
réimplémente le style de badge.py (BADGE_CSS) plutôt que d'appeler
ge_badge() : un composant CCv2 ne peut pas en imbriquer un autre dans
son propre rendu (cf. badge.py pour le détail).

À poser DANS un ge_surface() côté appelant pour la carte blanche avec
ombre (cf. Figma: Surface > liste bordée) — ge_list() ne fournit QUE
la liste bordée elle-même (border outline-variant, rounded-4px),
cohérent avec le reste du kit : composition, pas un composant monolithique
par écran.
"""

import streamlit as st
from .icons import ICON_FONT_CSS
from .badge import BADGE_CSS

_ge_list = st.components.v2.component(
    name="ge_list",
    html="""<div class="ge-list" id="ge-list"></div>""",
    css=ICON_FONT_CSS + BADGE_CSS + """
    .ge-list {
        display: flex;
        flex-direction: column;
        width: 100%;
        border: 1px solid var(--md-sys-color-outline-variant);
        border-radius: var(--md-sys-shape-corner-extra-small);
        overflow: hidden;
        font-family: var(--st-font, sans-serif);
        box-sizing: border-box;
    }
    .ge-list-item {
        display: flex;
        align-items: center;
        gap: 20px;
        width: 100%;
        min-height: 64px;
        padding: 12px 16px;
        background: var(--md-sys-color-surface);
        box-sizing: border-box;
        cursor: pointer;
        transition: background 0.12s;
    }
    .ge-list-item:hover {
        background: var(--md-sys-color-surface-container-low);
    }
    .ge-list-item-main {
        display: flex;
        flex: 1 0 0;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        min-width: 0;
    }
    .ge-list-item-text {
        display: flex;
        flex-direction: column;
        gap: 2px;
        min-width: 0;
    }
    .ge-list-item-code {
        font-size: var(--md-sys-typescale-body-small-size);
        line-height: var(--md-sys-typescale-body-small-line-height);
        letter-spacing: var(--md-sys-typescale-body-small-tracking);
        color: var(--md-sys-color-on-surface-variant);
    }
    .ge-list-item-title {
        font-size: var(--md-sys-typescale-label-large-size);
        line-height: var(--md-sys-typescale-label-large-line-height);
        font-weight: 500;
        color: var(--md-sys-color-on-surface);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .ge-list-item-arrow {
        flex-shrink: 0;
        font-size: 24px;
        color: var(--md-sys-color-on-surface-variant);
    }
    .ge-list-divider {
        height: 1px;
        background: var(--md-sys-color-outline-variant);
        flex-shrink: 0;
    }
    """,
    js="""
    export default function({ parentElement, data, setTriggerValue }) {
        const list = parentElement.querySelector('#ge-list');
        list.innerHTML = '';

        const items = data.items || [];
        items.forEach((item, index) => {
            const row = document.createElement('div');
            row.className = 'ge-list-item';

            const main = document.createElement('div');
            main.className = 'ge-list-item-main';

            const text = document.createElement('div');
            text.className = 'ge-list-item-text';
            if (item.code) {
                const code = document.createElement('span');
                code.className = 'ge-list-item-code';
                code.textContent = item.code;
                text.appendChild(code);
            }
            const title = document.createElement('span');
            title.className = 'ge-list-item-title';
            title.textContent = item.title || '';
            text.appendChild(title);
            main.appendChild(text);

            if (item.status_label) {
                const badge = document.createElement('span');
                badge.className = 'ge-badge ' + (item.status_variant || 'neutral');
                badge.textContent = item.status_label;
                main.appendChild(badge);
            }

            row.appendChild(main);

            const arrow = document.createElement('span');
            arrow.className = 'ge-list-item-arrow material-symbols-outlined';
            arrow.textContent = 'arrow_forward';
            row.appendChild(arrow);

            row.onclick = () => setTriggerValue('selected', item.id);
            list.appendChild(row);

            if (index < items.length - 1) {
                const divider = document.createElement('div');
                divider.className = 'ge-list-divider';
                list.appendChild(divider);
            }
        });
    }
    """,
)


def ge_list(items: list[dict], key: str = "ge_list"):
    """
    Affiche une liste cliquable GE-DESIGN, pleine largeur, bordée,
    avec badge de statut et flèche de navigation par ligne.

    items: liste de dicts {id, title, code?, status_label?,
    status_variant?} — `code` (petit libellé gris au-dessus du titre)
    et le badge (`status_label`/`status_variant`, cf. badge.py pour
    les variantes) sont optionnels.
    Retourne l'id de l'item cliqué durant CE run (ou `None`).

    Exemple :
        selected = ge_list(
            items=[
                {
                    "id": "gc2028", "code": "202803EL-GC",
                    "title": "Grand Conseil 2028",
                    "status_label": "Non démarrée", "status_variant": "neutral",
                },
                {
                    "id": "av2028", "code": "202803EL-AV",
                    "title": "Election Aire-la-Ville",
                    "status_label": "Analysée", "status_variant": "success",
                },
            ],
            key="scrutin_groups",
        )
        if selected:
            st.session_state.current_group = selected
            st.rerun()
    """
    result = _ge_list(key=key, data={"items": items}, on_selected_change=lambda: None)
    return result.selected
