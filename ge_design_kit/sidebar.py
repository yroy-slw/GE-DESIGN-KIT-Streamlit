"""
ge_design_kit.sidebar
-----------------------
Sidebar de navigation GE-DESIGN (pattern SuisseVote / MemIA : liste
d'items icône + libellé, item actif surligné, groupes optionnels).

Le composant remonte l'id de l'item cliqué via st.session_state
(pattern trigger CCv2 st.switch_page, ou simple routing par état).
"""

import streamlit as st
from .icons import ICON_FONT_CSS

_ge_sidebar = st.components.v2.component(
    name="ge_sidebar",
    html="""<nav class="ge-sidebar" id="ge-sidebar"></nav>""",
    css=ICON_FONT_CSS + """
    .ge-sidebar {
        display: flex;
        flex-direction: column;
        gap: 0;
        background: var(--md-sys-color-surface-container-low);
        padding: calc(var(--spacing) * 4) 0;
        font-family: var(--st-font, sans-serif);
        min-height: 100%;
        box-sizing: border-box;
    }
    .ge-sidebar-title {
        font-size: var(--md-sys-typescale-title-large-size);
        font-weight: 600;
        color: var(--md-sys-color-on-surface);
        padding: 0 calc(var(--spacing) * 4);
        margin-bottom: calc(var(--spacing) * 5);
    }
    .ge-sidebar-item {
        display: flex;
        align-items: center;
        gap: calc(var(--spacing) * 2);
        padding: 16px 24px;
        margin: 0 !important;
        border-radius: 50px;
        font-size: var(--md-sys-typescale-label-medium-size);
        font-weight: 500;
        line-height: var(--md-sys-typescale-label-medium-line-height);
        letter-spacing: var(--md-sys-typescale-label-medium-tracking);
        color: var(--md-sys-color-on-surface-variant);
        cursor: pointer;
        transition: background 0.12s, color 0.12s;
        user-select: none;
    }
    .ge-sidebar-item:hover {
        color: var(--md-sys-color-on-surface);
    }
    .ge-sidebar-item.active {
        background: var(--md-sys-color-secondary-container);
        color: var(--md-sys-color-on-secondary-container);
        font-weight: 500;
    }
    .ge-sidebar-item .icon {
        font-size: 20px;
        width: 20px;
        text-align: center;
        flex-shrink: 0;
        color: currentColor;
    }
    .ge-sidebar-item .chevron {
        margin-left: auto;
        font-size: 18px;
        opacity: 0.6;
        color: currentColor;
    }
    .ge-sidebar-divider {
        height: 1px;
        background: var(--md-sys-color-outline-variant);
        margin: calc(var(--spacing) * 3) calc(var(--spacing) * 4);
    }
    """,
    js="""
    export default function({ parentElement, data, setTriggerValue }) {
        const nav = parentElement.querySelector('#ge-sidebar');
        nav.innerHTML = '';

        if (data.title) {
            const title = document.createElement('div');
            title.className = 'ge-sidebar-title';
            title.textContent = data.title;
            nav.appendChild(title);
        }

        (data.items || []).forEach((item) => {
            if (item.divider) {
                const div = document.createElement('div');
                div.className = 'ge-sidebar-divider';
                nav.appendChild(div);
                return;
            }
            const el = document.createElement('div');
            el.className = 'ge-sidebar-item' + (item.id === data.active_id ? ' active' : '');

            // DOM methods + textContent, jamais innerHTML avec des
            // données concaténées — item.label/item.icon viennent de
            // l'appelant Python et ne doivent jamais être interprétés
            // comme du HTML (cf. Pièges à connaître dans le README).
            const iconSpan = document.createElement('span');
            iconSpan.className = 'icon material-symbols-outlined';
            iconSpan.textContent = item.icon || '';
            el.appendChild(iconSpan);

            const labelSpan = document.createElement('span');
            labelSpan.textContent = item.label || '';
            el.appendChild(labelSpan);

            if (item.has_children) {
                const chevron = document.createElement('span');
                chevron.className = 'chevron material-symbols-outlined';
                chevron.textContent = 'chevron_right';
                el.appendChild(chevron);
            }

            el.onclick = () => setTriggerValue('selected', item.id);
            nav.appendChild(el);
        });
    }
    """,
)


def ge_sidebar(items: list[dict], title: str = "", active_id: str = "", key: str = "ge_sidebar"):
    """
    Affiche une sidebar de navigation GE-DESIGN.

    items: liste de dicts {id, label, icon, has_children?} ou {divider: True}
    `icon` attend un NOM d'icône Material Symbols (ex: "search", "settings").
    Retourne l'id de l'item cliqué durant ce run (ou None).

    Exemple :
        selected = ge_sidebar(
            items=[
                {"id": "operation", "label": "Opération", "icon": "add_circle"},
                {"id": "configuration", "label": "Configuration", "icon": "settings"},
                {"divider": True},
                {"id": "analyse", "label": "Analyse", "icon": "scatter_plot", "has_children": True},
                {"id": "recherche", "label": "Recherche", "icon": "search"},
            ],
            active_id="operation",
            key="main_sidebar",
        )
        if selected:
            st.session_state.current_page = selected
    """
    result = _ge_sidebar(
        key=key,
        data={"title": title, "items": items, "active_id": active_id},
        on_selected_change=lambda: None,
    )
    return result.selected
