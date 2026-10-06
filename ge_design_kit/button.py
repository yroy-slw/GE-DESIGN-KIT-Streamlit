"""
ge_design_kit.button
-----------------------
Composant "Button" GE-DESIGN — remplace st.button() enveloppé dans un
st.container(key=f"{PREFIX}...") avec des overrides CSS globaux par
variante (cf. gallery.py, FILLED_BUTTON_KEY_PREFIX etc.) par un vrai
composant CCv2 isolé (Shadow DOM), la variante passée en prop plutôt
que devinée depuis un préfixe de clé de conteneur.

Variantes (vocabulaire Material Design 3, cf. gallery.py) :
    "filled"    fond plein couleur primary — action principale
    "icon"      rond, icône seule, fond plein primary
    "outlined"  contour fin, fond transparent — action secondaire
    "text"      pas de bordure ni de fond — action discrète
"""

import streamlit as st

_ge_button = st.components.v2.component(
    name="ge_button",
    html="""
    <button id="ge-btn" class="ge-btn" type="button">
        <span id="ge-btn-icon" class="ge-btn-icon"></span>
        <span id="ge-btn-label" class="ge-btn-label"></span>
    </button>
    """,
    css="""
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

    .ge-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 0.4em;
        border: none;
        border-radius: var(--md-sys-shape-corner-full, 999px);
        padding: 0.7em 1.2em;
        font-family: var(--st-font);
        font-size: var(--md-sys-typescale-label-medium-size, 0.9rem);
        font-weight: 400;
        cursor: pointer;
        transition: opacity 0.15s, background 0.15s, border-color 0.15s;
    }
    .ge-btn:disabled {
        cursor: not-allowed;
        opacity: 0.5;
    }
    .ge-btn-icon.material-symbols-outlined {
        font-family: 'Material Symbols Outlined';
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        font-size: 1.2em;
        line-height: 1;
    }
    .ge-btn-icon:empty,
    .ge-btn-label:empty {
        display: none;
    }

    /* filled — action principale */
    .ge-btn--filled {
        background: var(--md-sys-color-primary, var(--st-primary-color));
        color: var(--md-sys-color-on-primary, white);
    }
    .ge-btn--filled:hover:not(:disabled) { opacity: 0.9; }

    /* icon — rond, icône seule */
    .ge-btn--icon {
        background: var(--md-sys-color-primary, var(--st-primary-color));
        color: var(--md-sys-color-on-primary, white);
        padding: 0.6em;
        border-radius: 999px;
        aspect-ratio: 1 / 1;
    }
    .ge-btn--icon .ge-btn-label { display: none; }
    .ge-btn--icon:hover:not(:disabled) { opacity: 0.9; }

    /* outlined — action secondaire */
    .ge-btn--outlined {
        background: transparent;
        color: var(--md-sys-color-primary, var(--st-primary-color));
        border: 1px solid var(--md-sys-color-outline, currentColor);
    }
    .ge-btn--outlined:hover:not(:disabled) {
        background: color-mix(in srgb, var(--md-sys-color-primary, currentColor) 8%, transparent);
    }

    /* text — action discrète */
    .ge-btn--text {
        background: transparent;
        color: var(--md-sys-color-primary, var(--st-primary-color));
        padding-inline: 0.7em;
    }
    .ge-btn--text:hover:not(:disabled) {
        background: color-mix(in srgb, var(--md-sys-color-primary, currentColor) 8%, transparent);
    }
    """,
    js="""
    export default function(component) {
        const { data, setTriggerValue, parentElement } = component;

        const btn = parentElement.querySelector("#ge-btn");
        const iconEl = parentElement.querySelector("#ge-btn-icon");
        const labelEl = parentElement.querySelector("#ge-btn-label");

        btn.className = "ge-btn ge-btn--" + (data.variant || "filled");
        btn.disabled = !!data.disabled;
        labelEl.textContent = data.label || "";

        // Même logique de détection ":material/xxx:" que ge_card —
        // cf. le fix Material Symbols côté card.py.
        const icon = data.icon || "";
        const materialMatch = /^:material\\/([a-z0-9_]+):$/.exec(icon);
        if (materialMatch) {
            iconEl.classList.add("material-symbols-outlined");
            iconEl.textContent = materialMatch[1];
        } else {
            iconEl.classList.remove("material-symbols-outlined");
            iconEl.textContent = icon;
        }

        // Bouton icône seule -> aria-label requis (accessibilité,
        // lecteurs d'écran) puisque le label visuel est masqué en CSS.
        if (data.variant === "icon" && data.label) {
            btn.setAttribute("aria-label", data.label);
        } else {
            btn.removeAttribute("aria-label");
        }

        btn.onclick = () => {
            if (btn.disabled) return;
            setTriggerValue("clicked", true);
        };
    }
    """,
)


def ge_button(label: str = "", *, variant: str = "filled", icon: str = "",
              disabled: bool = False, key: str = "ge_button",
              on_click=lambda: None) -> bool:
    """
    Affiche un bouton GE-DESIGN. Retourne True le run où il a été
    cliqué (sinon False) — même contrat que st.button().

    variant : "filled" | "icon" | "outlined" | "text"
    icon    : ":material/nom_icone:" (cf. fonts.google.com/icons,
              variante Outlined) ou un emoji brut.

    Exemple :
        if ge_button("Télécharger", variant="filled",
                      icon=":material/file_download:", key="btn_dl"):
            st.write("Téléchargement lancé")

        # Icône seule (rond) — passer quand même `label` pour
        # l'accessibilité, même s'il n'est pas affiché visuellement :
        ge_button("Rechercher", variant="icon",
                   icon=":material/search:", key="btn_search")
    """
    result = _ge_button(
        data={
            "label": label,
            "variant": variant,
            "icon": icon,
            "disabled": disabled,
        },
        key=key,
        on_clicked_change=on_click,
    )
    return bool(result.clicked)