"""
views/comparaison.py
-----------------------
Page "Comparer" - atteinte depuis views/operations.py en sélectionnant
des lignes du tableau puis en cliquant "Comparer". Lit
st.session_state.selected_operation_ids plutôt que de recevoir les
lignes en paramètre: c'est cet état, PAS les données elles-mêmes, qui
doit survivre st.switch_page() cf. data.py pour pourquoi refetch par
id plutôt que stocker les lignes sélectionnées telles quelles.
"""

import streamlit as st

from data import load_operations_df
from ge_design_kit import ge_breadcrumb, ge_surface

ge_breadcrumb(items=[
    {"id": "home", "label": "Accueil"},
    {"id": "comparaison", "label": "Comparer des opérations"},
])
st.title("Comparer des opérations")

selected_ids = st.session_state.get("selected_operation_ids", [])

if not selected_ids:
    # Pas de surface ici: rien à mettre dedans, l'alerte seule suffit
    # (cf. views/export.py, même choix).
    st.warning(
        "Aucune opération sélectionnée. Retournez à la page "
        "Opération, cochez des lignes dans le tableau, puis cliquez "
        "\"Comparer\"."
    )
else:
    with ge_surface("comparaison"):
        df = load_operations_df()
        compared_df = df[df["id"].isin(selected_ids)].drop(columns=["id"])
        st.write(f"**{len(compared_df)} opération(s) sélectionnée(s) :**")
        st.dataframe(compared_df, hide_index=True, width="stretch")
