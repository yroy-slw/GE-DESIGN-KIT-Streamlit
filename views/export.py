"""
views/export.py
------------------
Page "Exporter" - même pattern que comparaison.py: lit
st.session_state.selected_operation_ids, refetch les vraies données
par id (cf. data.py) plutôt que de recevoir les lignes en état.
"""

import streamlit as st

from data import load_operations_df
from ge_design_kit import ge_breadcrumb, ge_surface, FILLED_BUTTON_KEY_PREFIX

ge_breadcrumb(items=[
    {"id": "home", "label": "Accueil"},
    {"id": "export", "label": "Exporter des opérations"},
])
st.title("Exporter des opérations")

selected_ids = st.session_state.get("selected_operation_ids", [])

if not selected_ids:
    # Pas de surface ici: rien à mettre dedans, l'alerte seule suffit
    # (cf. views/comparaison.py, même choix).
    st.warning(
        "Aucune opération sélectionnée. Retournez à la page "
        "Opération, cochez des lignes dans le tableau, puis cliquez "
        "\"Exporter\"."
    )
else:
    with ge_surface("export"):
        df = load_operations_df()
        export_df = df[df["id"].isin(selected_ids)].drop(columns=["id"])
        st.write(f"**{len(export_df)} opération(s) prête(s) à l'export :**")
        st.dataframe(export_df, hide_index=True, width="stretch")
        # Action principale de l'écran -> bouton filled (M3), pas outlined
        with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}download_csv"):
            st.download_button(
                "Télécharger en csv",
                icon=":material/file_download:",
                data=export_df.to_csv(index=False).encode("utf-8"),
                file_name="operations_export.csv",
                mime="text/csv",
            )
