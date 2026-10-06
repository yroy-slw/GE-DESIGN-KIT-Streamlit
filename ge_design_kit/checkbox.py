"""
ge_design_kit.checkbox
-------------------------
Composant "Checkbox" GE-DESIGN - remplace st.checkbox() enveloppé dans
un st.container(key=...) avec des overrides CSS globaux (fragile, cf.
gallery.py) par un vrai composant CCv2 isolé (Shadow DOM), paramétrable
et dont l'état persiste correctement entre les reruns.
"""

import streamlit as st

_ge_checkbox = st.components.v2.component(
    name="ge_checkbox",
    html="""
    <label class="ge-checkbox-container">
        <input type="checkbox" id="ge-checkbox-input" />
        <span id="ge-checkbox-label"></span>
    </label>
    """,
    css="""
    .ge-checkbox-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: var(--st-font);
        color: var(--md-sys-color-on-surface, var(--st-text-color));
        cursor: pointer;
    }
    #ge-checkbox-input {
        accent-color: var(--md-sys-color-primary, var(--st-primary-color));
        width: 20px;
        height: 20px;
        cursor: pointer;
    }
    """,
    js="""
    export default function(component) {
        const { data, setStateValue, parentElement } = component;

        const input = parentElement.querySelector("#ge-checkbox-input");
        const label = parentElement.querySelector("#ge-checkbox-label");

        label.textContent = data.label || "";
        if (input.checked !== data.checked) {
            input.checked = data.checked ?? false;
        }

        // "checked" est une valeur PERSISTANTE (contrairement à un clic
        // de bouton, événement ponctuel) -> setStateValue, pas
        // setTriggerValue.
        input.onchange = () => {
            setStateValue("checked", input.checked);
        };
    }
    """,
)


def ge_checkbox(label: str, checked: bool = False, key: str = "ge_checkbox",
                 on_change=lambda: None) -> bool:
    """
    Affiche une case à cocher GE-DESIGN. Retourne l'état coché actuel
    (bool), qui persiste entre les reruns via st.session_state[key] —
    pas besoin de gérer toi-même la mémorisation côté appelant.

    Exemple :
        is_checked = ge_checkbox("Activer la fonctionnalité",
                                   checked=True, key="feature_flag")
        if is_checked:
            st.write("Fonctionnalité activée")
    """
    # Une fois monté au moins une fois avec ce key, l'état vit dans
    # st.session_state[key] — on le relit pour ne pas retomber sur
    # `checked` (juste la valeur par défaut à l'appel) à chaque rerun.
    component_state = st.session_state.get(key, {})
    current_value = component_state.get("checked", checked)

    result = _ge_checkbox(
        data={"label": label, "checked": current_value},
        default={"checked": checked},
        key=key,
        on_checked_change=on_change,
    )
    return bool(result.checked)