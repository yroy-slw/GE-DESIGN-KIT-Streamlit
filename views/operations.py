import streamlit as st

from data import load_operations_df
from ge_design_kit import (
    ge_breadcrumb, ge_surface, ge_label_spacer, ICON_BUTTON_KEY_PREFIX,
    PILL_BUTTON_KEY_PREFIX, TEXT_BUTTON_KEY_PREFIX, ge_kpi, GE_TOGGLE_KEY_PREFIX,
)

# ── Compteur de sélection (placeholder — sera piloté par les cases à
# cocher du futur tableau d'opérations) ──
if "selected_count" not in st.session_state:
    st.session_state.selected_count = 0
# ── Compteur de reset : incrémenté à chaque clic sur "Annuler la
# sélection". Utilisé pour construire une clé DYNAMIQUE pour
# st.dataframe (cf. table_key plus bas), changer la clé force
# Streamlit à traiter le tableau comme un widget entièrement NOUVEAU,
# sans aucun état résiduel. Plus robuste que réécrire directement
# st.session_state["operations_table"] : cette dernière approche
# fonctionnait la première fois mais pas la seconde (Streamlit semble
# garder un état de sélection interne qu'un simple écrasement du
# dict ne suffit pas à effacer de façon fiable et répétée). ──
if "operations_table_reset_counter" not in st.session_state:
    st.session_state.operations_table_reset_counter = 0

# ── Contenu principal : plein-largeur (plus de st.columns pour la sidebar) ──
ge_breadcrumb(items=[
    {"id": "home", "label": "Accueil"},
    {"id": "operations", "label": "Sélectionner une opération"},
])

with st.container(key="ge-header-row"):
    title_col, action_col = st.columns([5, 2], vertical_alignment="top")
with title_col:
    st.title("Sélectionner une opération")
with action_col:
    # Alignement à droite géré par layout.py — cf. règle CSS
    # .st-key-ge-header-row [data-testid="stColumn"]:last-child.
    # Pas besoin de colonne interne ni de width="stretch" : le bouton
    # est toujours width:auto (cf. buttons.py), stretch n'aurait aucun
    # effet visible.
    with st.container(key=f"{PILL_BUTTON_KEY_PREFIX}import_manuel"):
        import_clicked = st.button(
            "Importer manuellement",
            icon=":material/upload:",
            key="btn_import_manuel",
        )


@st.dialog("Importer manuellement")
def _import_manuel_dialog():
    # Contenu pas encore validé (maquette Figma fournie à titre
    # d'exemple, cf. ge_design_kit/dialog.py) — placeholder en
    # attendant. Le style du modal (fond, coins, ombre, titre) est
    # déjà branché sur GE-DESIGN via inject_ge_styles().
    st.info("Contenu à définir.")


if import_clicked:
    _import_manuel_dialog()

# ── Tout le contenu de la page vit dans UNE seule carte GE-DESIGN ──
with ge_surface("operations"):
    st.subheader("Choisir la votation à analyser")

    with ge_surface("kpi-row", variant="inset"):
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            ge_kpi(4, "Opérations disponibles", key="kpi_total")
        with c2:
            ge_kpi(2, "Analyses terminées", key="kpi_done")
        with c3:
            ge_kpi(1, "Analyse en cours", key="kpi_progress")
        with c4:
            ge_kpi(1, "Non démarrée", key="kpi_none")
        with c5:
            ""  # colonne vide pour l'espacement

        st.divider()

        # ── Ligne de filtres : widgets natifs, stylés via forms.py ──
        with st.container(key="ge-filter-row"):
            fc1, fc3, fc4, fc5, fc6 = st.columns([3.6, 1.3, 1.3, 1.3, 1.8])
            with fc1:
                # st.form lie le champ et le bouton : Entrée dans le champ
                # déclenche la même soumission qu'un clic sur le bouton
                with st.form(key="search-form", border=False):
                    ic1, ic2 = st.columns([5, 1])
                    with ic1:
                        search_term = st.text_input(
                            "Rechercher une opération",
                            placeholder="Rechercher une opération...",
                            key="op_search",
                        )
                    with ic2:
                        with st.container(key=f"{ICON_BUTTON_KEY_PREFIX}search"):
                            ge_label_spacer()
                            searched = st.form_submit_button("", icon=":material/search:")
                    if searched:
                        st.session_state.last_search = search_term
            with fc3:
                scrutin_type = st.selectbox(
                    "Type de scrutin",
                    options=["Tous", "Votation", "Élection"],
                    key="filter_scrutin",
                )
            with fc4:
                date_filter = st.selectbox(
                    "Date",
                    options=["Tous", "17.06.2025", "09.02.2025", "22.10.2025"],
                    key="filter_date",
                )
            with fc5:
                canal_filter = st.selectbox(
                    "Canal",
                    options=["Tous", "Correspondance", "Urne"],
                    key="filter_canal",
                )
            with fc6:
                with st.container(key=f"{GE_TOGGLE_KEY_PREFIX}filter_done"):
                    show_done = st.toggle("Opérations terminées", value=True, key="filter_done")

    # ── Barre de sélection : réservée ICI visuellement ──
    selection_bar_slot = st.empty()

    # ── Tableau des opérations : st.dataframe natif avec sélection ──
    # réelle (checkboxes gérées par Streamlit, aucun CSS custom). ──
    # data.py fournit une colonne "id" stable — indispensable pour que
    # la sélection survive la navigation vers Comparer/Exporter (cf.
    # data.py pour le pourquoi complet).
    operations_df = load_operations_df()

    # ── Application des filtres de la ligne au-dessus (recherche/type/ ──
    # date/canal/toggle) sur les données AVANT de les passer au tableau. ──
    filtered_df = operations_df.copy()

    # Recherche : n'applique que le terme SOUMIS (via Entrée ou clic sur
    # la loupe, cf. st.form plus haut) — pas de filtrage à chaque frappe.
    search_value = st.session_state.get("last_search", "")
    if search_value:
        filtered_df = filtered_df[
            filtered_df["Opération"].str.contains(search_value, case=False, na=False)
        ]

    if scrutin_type != "Tous":
        filtered_df = filtered_df[filtered_df["Type de scrutin"] == scrutin_type]
    if date_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Date"] == date_filter]

    if canal_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Canal"] == canal_filter]

    # "Opérations terminées" OFF (défaut) : cache les opérations déjà
    # analysées — l'utilisateur voit d'abord ce qui demande son attention.
    if not show_done:
        filtered_df = filtered_df[~filtered_df["Statut analyse"].str.contains("Analysée")]

    # display_df garde la colonne "id" (nécessaire pour retrouver les
    # lignes cochées par leur identité stable, pas leur position — cf.
    # data.py) mais ne l'affiche PAS : column_order plus bas liste
    # explicitement les colonnes visibles, "id" n'y figure pas.
    display_df = filtered_df.drop(columns=["Type de scrutin", "Canal"])

    # La clé change à chaque reset (cf. operations_table_reset_counter
    # tout en haut du fichier), Streamlit traite alors le tableau comme
    # un nouveau widget, sans aucune sélection résiduelle possible.
    table_key = f"operations_table_{st.session_state.operations_table_reset_counter}"

    event = st.dataframe(
        display_df,
        key=table_key,
        hide_index=True,
        width="stretch",
        on_select="rerun",
        selection_mode="multi-row",
        column_order=["Opération", "Date", "Statut analyse", "Clusters", "Dernière analyse"],
        column_config={
            "Opération": st.column_config.TextColumn("Opération", width="large"),
            "Clusters": st.column_config.NumberColumn("Clusters", format="%d"),
        },
    )

    # event.selection.rows = index DE POSITION dans display_df pour CE
    # run — jamais stockés tels quels (cf. data.py) : convertis
    # immédiatement en id stables via .iloc + colonne "id".
    selected_rows = event.selection.rows
    selected_ids = display_df.iloc[selected_rows]["id"].tolist() if selected_rows else []
    st.session_state.selected_count = len(selected_rows)
    count = st.session_state.selected_count

    # ── Remplissage du placeholder réservé plus haut, avec le compte ──
    # à jour de CE run — même structure/CSS qu'avant, juste déplacée. ──
    with selection_bar_slot.container():
        with ge_surface("selection-bar", variant="inset"):
            with st.container(key="ge-selection-bar-row"):
                sb_left, sb_right = st.columns(2)
                with sb_left:
                    st.markdown(f"**Nombre d'opération(s) sélectionnée(s) : {count}**")
                    with st.container(key=f"{TEXT_BUTTON_KEY_PREFIX}clear_selection"):
                        if st.button(
                            "Annuler la sélection",
                            icon=":material/close:",
                            type="tertiary",
                            disabled=(count == 0),
                            key="btn_clear_selection",
                        ):
                            # Incrémente le compteur -> la clé du tableau change au
                            # prochain run -> Streamlit le recrée comme un widget
                            # tout neuf, sans sélection résiduelle possible.
                            st.session_state.operations_table_reset_counter += 1
                            st.rerun()
                with sb_right:
                    with st.container(key="ge-button-group"):
                        with st.container(key=f"{PILL_BUTTON_KEY_PREFIX}compare"):
                            if st.button(
                                "Comparer",
                                type="secondary",
                                disabled=(count == 0),
                                key="btn_compare",
                            ):
                                # session_state, pas les lignes elles-mêmes : la
                                # page de destination refetch par id (cf. data.py
                                # et views/comparaison.py).
                                st.session_state.selected_operation_ids = selected_ids
                                st.switch_page("views/comparaison.py")
                        with st.container(key=f"{PILL_BUTTON_KEY_PREFIX}export"):
                            if st.button(
                                "Exporter",
                                type="secondary",
                                disabled=(count == 0),
                                key="btn_export",
                            ):
                                st.session_state.selected_operation_ids = selected_ids
                                st.switch_page("views/export.py")
