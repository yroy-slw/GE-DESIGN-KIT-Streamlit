"""
ge_design_kit.card
-------------------
Composant "Card" réutilisable, thémé via les variables --st-* injectées
par Streamlit (CCv2). A copier tel quel dans un autre projet Streamlit :
seul le fichier .streamlit/config.toml doit être aligné sur GE-DESIGN
pour que le rendu soit cohérent.
"""

import streamlit as st

_ge_card = st.components.v2.component(
    name="ge_card",
    html="""
    <div class="ge-card">
        <div class="ge-card-header">
            <span class="ge-card-icon" id="ge-card-icon"></span>
            <h3 class="ge-card-title" id="ge-card-title"></h3>
        </div>
        <p class="ge-card-content" id="ge-card-content"></p>
        <button class="ge-card-button" id="ge-card-button"></button>
    </div>
    """,
    css="""
    .ge-card {
        background: var(--md-sys-color-surface, var(--st-secondary-background-color));
        border-radius: var(--md-sys-shape-corner-medium, var(--st-base-radius));
        padding: calc(var(--spacing, 4px) * 6) calc(var(--spacing, 4px) * 6);
        font-family: var(--st-font);
        font-size: var(--md-sys-typescale-body-medium-size, var(--st-base-font-size));
        display: flex;
        flex-direction: column;
        gap: calc(var(--spacing, 4px) * 2);
        /* Elevation shadow/2 */
        box-shadow:
            0 1px 2px 0 rgba(24, 31, 37, 0.30),
            0 1px 6px 2px rgba(24, 31, 37, 0.15);
    }
    .ge-card-header {
        display: flex;
        align-items: center;
        gap: calc(var(--spacing, 4px) * 2);
    }
    .ge-card-icon {
        font-size: 1.1em;
    }
    .ge-card-title {
        color: var(--md-sys-color-on-surface);
        font-size: var(--md-sys-typescale-title-large-size, 1.05em);
        font-weight: 600;
        margin: 0;
    }
    .ge-card-content {
        color: var(--md-sys-color-on-surface-variant);
        line-height: 1.5;
        margin: 0;
    }
    .ge-card-button {
        align-self: flex-start;
        background: var(--md-sys-color-primary);
        color: var(--md-sys-color-on-primary, white);
        border: none;
        border-radius: var(--md-sys-shape-corner-full, 999px);
        padding: calc(var(--spacing, 4px) * 2.5) calc(var(--spacing, 4px) * 4);
        font-size: var(--md-sys-typescale-label-medium-size, 0.85em);
        font-weight: 500;
        cursor: pointer;
        transition: opacity 0.15s;
    }
    .ge-card-button:hover { opacity: 0.85; }
    .ge-card-button:empty { display: none; }
    """,
    js="""
    export default function({ parentElement, data, setTriggerValue }) {
        const el = parentElement.querySelector('.ge-card');
        el.querySelector('#ge-card-icon').textContent = data.icon || '';
        el.querySelector('#ge-card-title').textContent = data.title || '';
        el.querySelector('#ge-card-content').textContent = data.content || '';

        const btn = el.querySelector('#ge-card-button');
        if (data.button_label) {
            btn.textContent = data.button_label;
            btn.onclick = () => setTriggerValue('clicked', data.key || 'ge_card');
        }
    }
    """,
)


def ge_card(title: str, content: str, icon: str = "", button_label: str = "", key: str = "ge_card"):
    """
    Affiche une card GE-DESIGN. Retourne True si le bouton a été cliqué
    durant ce run (sinon False).

    Exemple :
        if ge_card("Opérations", "4 disponibles", icon="🗳️",
                    button_label="Voir", key="card_ops"):
            st.write("Carte cliquée !")
    """
    result = _ge_card(
        key=key,
        data={"title": title, "content": content, "icon": icon,
              "button_label": button_label, "key": key},
        on_clicked_change=lambda: None,
    )
    return bool(result.clicked)
