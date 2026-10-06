"""
Galerie de composants GE-Design-kit — outil de développement autonome,
PAS une page de l'app MemIA (app.py a sa propre navigation simulée via
ge_sidebar + session_state, pas de vraie navigation multipage
Streamlit — cf. sa docstring). Se lance séparément :

    streamlit run gallery.py

Chaque section montre le rendu réel du composant ET le code Python
exact qui l'a produit (via inspect.getsource — le snippet affiché ne
peut donc jamais diverger silencieusement de ce qui a vraiment tourné).
"""

import inspect
import textwrap

import streamlit as st

from ge_design_kit import (
    inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar, ge_breadcrumb, ge_surface,
    ge_card, ge_kpi, ge_stepper, ge_sidebar, ge_label_spacer, ge_badge, ge_list,
    FILLED_BUTTON_KEY_PREFIX, ICON_BUTTON_KEY_PREFIX, OUTLINED_BUTTON_KEY_PREFIX,
    TEXT_BUTTON_KEY_PREFIX, GE_TOGGLE_KEY_PREFIX, GE_CHEKBOX_KEY_PREFIX,
)

_GALLERY_SECTIONS = [
    ("topbar", "Topbar"),
    ("sidebar", "Sidebar"),
    ("breadcrumb", "Breadcrumb"),
    ("surface", "Surface"),
    ("card", "Card"),
    ("kpi", "KPI"),
    ("badge", "Badge"),
    ("liste", "Liste"),
    ("boutons", "Boutons"),
    ("checkbox-et-toggle", "Checkbox et Toggle"),
    ("modal", "Modal"),
    ("alertes", "Alertes"),
    ("typographie", "Typographie"),
    ("widgets-natifs-stylés-automatiquement", "Widgets natifs"),
]

# ── Mode rail de la sidebar (icônes seules) — piloté par le burger de
# ge_topbar, cf. app.py pour le pattern complet (c'est le même ici,
# gallery.py le démontre en conditions réelles plutôt qu'en pseudo-code
# dans demo_ge_topbar()/demo_ge_sidebar() plus bas). ──
if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False


def _toggle_sidebar():
    st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed


st.set_page_config(page_title="GE-Design-kit — Galerie de composants", layout="wide")
inject_ge_styles(sidebar_collapsed=st.session_state.sidebar_collapsed)

with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="GE-Design-kit", user_label="Galerie", on_toggle=_toggle_sidebar)

with st.container(key="wrapper_gallery_container"):  # slot pour le contenu réel de la galerie

    with st.container(key="main_gallery_container"):  # slot pour le contenu réel de la galerie

        def show_example(func):
            """
            Exécute `func()` (le rendu réel du composant) puis affiche son
            propre code source en dessous, dédenté et sans la ligne `def ...:`
            — un snippet directement copiable dans une vraie app.
            """
            func()
            source = inspect.getsource(func)
            lines = source.splitlines()[1:]  # retire la ligne "def demo_xxx():"
            body = textwrap.dedent("\n".join(lines))
            st.code(body, language="python")


        st.title("Galerie de composants GE-Design-kit")
        st.caption(
            "Référence visuelle + code d'intégration pour chaque composant du kit."
        )
        st.divider()

        # ── Topbar ────────────────────────────────────────────────────────────
        st.header("Topbar", anchor="topbar")
        st.write(
            "Bandeau institutionnel fixe en haut de l'app. Déjà affiché tout en "
            "haut de cette page — voir le code ci-dessous. Le burger à gauche "
            "bascule le mode rail de la sidebar (cf. section Sidebar plus bas) "
            "via `on_toggle` — essayez-le, il pilote la VRAIE sidebar de cette "
            "page, pas une démo isolée."
        )


        def demo_ge_topbar():
            from ge_design_kit import inject_ge_styles, TOPBAR_SLOT_KEY, ge_topbar

            st.set_page_config(page_title="Mon app", layout="wide")

            if "sidebar_collapsed" not in st.session_state:
                st.session_state.sidebar_collapsed = False

            def toggle_sidebar():
                st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed

            # sidebar_collapsed assorti à ge_sidebar(collapsed=...) plus bas —
            # sinon la largeur de section[data-testid="stSidebar"] (pilotée ici)
            # et son contenu (piloté par ge_sidebar) divergent.
            inject_ge_styles(sidebar_collapsed=st.session_state.sidebar_collapsed)

            with st.container(key=TOPBAR_SLOT_KEY):
                ge_topbar(
                    app_name="GE", user_label="Mon compte", env="DEV",
                    on_toggle=toggle_sidebar,
                )


        st.code(
            textwrap.dedent("\n".join(inspect.getsource(demo_ge_topbar).splitlines()[1:])),
            language="python",
        )
        st.divider()

        # ── Sidebar ───────────────────────────────────────────────────────────
        st.header("Sidebar", anchor="sidebar")
        st.write(
            "Menu latéral de navigation — utilisé dans `st.sidebar` de cette même "
            "page (regardez à gauche). Retourne l'id de l'item cliqué durant CE "
            "run (ou `None`), à combiner avec `st.session_state` pour piloter la "
            "page active. `collapsed=True` bascule en mode rail (icônes seules, "
            "largeur de section[data-testid=\"stSidebar\"] à assortir côté "
            "layout.py) — cliquez le burger du topbar ci-dessus pour basculer "
            "la sidebar de CETTE page."
        )

        with st.sidebar:
            gallery_selected = ge_sidebar(
                items=[
                    {"id": "operation", "label": "Composants", "icon": "computer"},
                ],
                active_id="operation",
                collapsed=st.session_state.sidebar_collapsed,
                key="gallery_sidebar",
            )


        def demo_ge_sidebar():
            with st.sidebar:
                selected = ge_sidebar(
                    items=[
                        {"id": "operation", "label": "Opération", "icon": "add_circle"},
                        {"id": "configuration", "label": "Configuration", "icon": "settings"},
                        {"divider": True},
                        {"id": "analyse", "label": "Analyse", "icon": "scatter_plot", "has_children": True},
                        {"id": "recherche", "label": "Recherche", "icon": "search"},
                    ],
                    active_id=st.session_state.current_page,
                    collapsed=st.session_state.sidebar_collapsed,
                    key="main_sidebar",
                )
                if selected:
                    st.session_state.current_page = selected
                    st.rerun()


        st.code(
            textwrap.dedent("\n".join(inspect.getsource(demo_ge_sidebar).splitlines()[1:])),
            language="python",
        )
        st.divider()

        # ── Breadcrumb ────────────────────────────────────────────────────────
        st.header("Breadcrumb", anchor="breadcrumb")


        def demo_ge_breadcrumb():
            ge_breadcrumb(items=[
                {"id": "home", "label": "Accueil"},
                {"id": "operations", "label": "Sélectionner une opération"},
            ])


        show_example(demo_ge_breadcrumb)
        st.divider()

        # ── Surface ───────────────────────────────────────────────────────────
        st.header("Surface", anchor="surface")
        st.write(
            "Conteneur de page - contrairement à `ge_card`, peut contenir "
            "n'importe quel widget Streamlit. Deux variantes : `\"card\"` "
            "(fond blanc + ombre, défaut) et `\"inset\"` (fond teinté, sans "
            "ombre, pour sous-grouper du contenu dans une carte)."
        )


        def demo_ge_surface():
            with ge_surface("gallery-demo-surface"):
                st.write("Contenu dans une surface variant=\"card\" (défaut).")
                with ge_surface("gallery-demo-inset", variant="inset"):
                    st.write("Sous-bloc en variant=\"inset\".")


        show_example(demo_ge_surface)
        st.divider()

        # ── Card ──────────────────────────────────────────────────────────────
        st.header("Card", anchor="card")
        st.write(
            "Composant CCv2 figé (titre + texte + bouton optionnel) — ne peut "
            "PAS contenir d'autres widgets Streamlit (contrairement à "
            "`ge_surface`). Retourne `True` le run où le bouton est cliqué."
        )


        def demo_ge_card():
            clicked = ge_card(
                "Opérations",
                "4 disponibles",
                icon="🗳️",
                button_label="Voir",
                key="gallery_card",
            )
            if clicked:
                st.toast("Carte cliquée !")


        show_example(demo_ge_card)
        st.divider()

        # ── KPI ───────────────────────────────────────────────────────────────
        st.header("KPI", anchor="kpi")
        st.write("Card chiffre + libellé, purement d'affichage (pas d'interaction).")


        def demo_ge_kpi():
            c1, c2, c3 = st.columns(3)
            with c1:
                ge_kpi(4, "Opérations disponibles", key="gallery_kpi_1")
            with c2:
                ge_kpi(0, "Analyses terminées", key="gallery_kpi_2")
            with c3:
                ge_kpi(1, "Analyse en cours", key="gallery_kpi_3")


        show_example(demo_ge_kpi)
        st.caption(
            "Le 2ᵉ exemple vaut délibérément 0 — `ge_kpi` gère bien ce cas "
            "(un ancien bug affichait `0` comme une chaîne vide, cf. forms.py)."
        )
        st.divider()

        # ── Badge ─────────────────────────────────────────────────────────────
        st.header("Badge", anchor="badge")
        st.write(
            "Badge/chip de statut (Figma \"MD_Chips\", node 233:6752) — "
            "composant d'affichage pur, pas d'interaction, pas de retour. "
            "Réutilisable seul ou comme brique interne d'un autre composant "
            "(cf. `ge_list` ci-dessous, qui en affiche un par ligne)."
        )


        def demo_ge_badge():
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                ge_badge("Non démarrée", variant="neutral", key="gallery_badge_neutral")
            with b2:
                ge_badge("Analysée", variant="success", key="gallery_badge_success")
            with b3:
                ge_badge("En cours", variant="warning", key="gallery_badge_warning")
            with b4:
                ge_badge("Erreur", variant="error", key="gallery_badge_error")


        show_example(demo_ge_badge)
        st.divider()

        # ── Liste ─────────────────────────────────────────────────────────────
        st.header("Liste", anchor="liste")
        st.write(
            "Liste cliquable pleine largeur, bordée, avec badge de statut et "
            "flèche de navigation par ligne (Figma \"MD_List item "
            "transverse\", node 529:60163 — ex: \"Sélectionner un groupe de "
            "scrutins\"). Même pattern que `ge_sidebar`/`ge_breadcrumb` : "
            "liste d'items en Python, id de l'item cliqué remonté durant CE "
            "run (ou `None`). À poser dans un `ge_surface()` côté appelant "
            "pour la carte blanche avec ombre (cf. Figma : Surface > liste "
            "bordée) — `ge_list` ne fournit que la liste bordée elle-même."
        )


        def demo_ge_list():
            with ge_surface("gallery-demo-list"):
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
                    key="gallery_list",
                )
            if selected:
                st.toast(f"Ligne cliquée : {selected}")


        show_example(demo_ge_list)
        st.divider()

        # ── Boutons ───────────────────────────────────────────────────────────
        st.header("Boutons", anchor="boutons")
        st.write(
            "`st.button()` n'accepte pas de classe CSS personnalisée : le style "
            "passe par un **conteneur enveloppant** (`st.container(key=...)`), "
            "pas par le bouton lui-même. Quatre variantes, vocabulaire Material "
            "Design 3 :"
        )
        st.markdown(
            "- `FILLED_BUTTON_KEY_PREFIX` — fond plein couleur primary, libellé "
            "(ex : action principale d'un écran, \"Télécharger en CSV\")\n"
            "- `ICON_BUTTON_KEY_PREFIX` — bouton rond, icône seule, fond plein "
            "couleur primary (ex : bouton recherche rond)\n"
            "- `OUTLINED_BUTTON_KEY_PREFIX` — contour fin, fond transparent "
            "(ex : action secondaire)\n"
            "- `TEXT_BUTTON_KEY_PREFIX` — pas de bordure ni de fond, libellé "
            "coloré (ex : action discrète)"
        )


        def demo_buttons():
            b1, b2, b3, b4 = st.columns(4)
            with b1:
                with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}gallery_filled"):
                    st.button("Télécharger", icon=":material/file_download:", key="gallery_btn_filled")
            with b2:
                with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_outlined"):
                    st.button("Importer", icon=":material/upload:", key="gallery_btn_outlined")
            with b3:
                with st.container(key=f"{TEXT_BUTTON_KEY_PREFIX}gallery_text"):
                    st.button("Annuler", icon=":material/close:", key="gallery_btn_text")
            with b4:
                with st.container(key=f"{ICON_BUTTON_KEY_PREFIX}gallery_icon"):
                    st.button("", icon=":material/search:", key="gallery_btn_icon")


        show_example(demo_buttons)
        st.divider()

        st.subheader("ge_label_spacer")
        st.write(
            "`st.button` n'a pas de label au-dessus de lui, contrairement à "
            "`text_input`/`selectbox` — côte à côte, le bouton se retrouve plus "
            "haut que ses voisins. `ge_label_spacer(height_px=10)` comble cet "
            "écart. Comparaison, sans puis avec :"
        )


        def demo_label_spacer():
            s1, s2 = st.columns(2)
            with s1:
                st.caption("Sans spacer — mal aligné")
                a1, a2 = st.columns([3, 1])
                with a1:
                    st.text_input("Champ", key="gallery_spacer_input_bad")
                with a2:
                    with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_bad"):
                        st.button("OK", key="gallery_btn_bad")
            with s2:
                st.caption("Avec spacer — aligné")
                b1, b2 = st.columns([3, 1])
                with b1:
                    st.text_input("Champ", key="gallery_spacer_input_good")
                with b2:
                    with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_good"):
                        ge_label_spacer()
                        st.button("OK", key="gallery_btn_good")


        show_example(demo_label_spacer)
        st.divider()

        # ── Checkbox et Toggle ────────────────────────────────────────────────
        st.header("Checkbox et Toggle", anchor="checkbox-et-toggle")
        st.write(
            "`st.checkbox` et `st.toggle` sont le **même composant** côté "
            "Streamlit (même `data-testid`). Un `st.checkbox` **non enveloppé** "
            "s'affiche en case à cocher standard par défaut — c'est "
            "`st.toggle` qui a besoin d'être explicitement enveloppé dans "
            "`GE_TOGGLE_KEY_PREFIX` pour devenir un switch, sinon il "
            "hériterait de l'apparence case-à-cocher."
        )


        def demo_checkbox_toggle():
            col1, col2 = st.columns(2)
            with col1:
                with st.container(key=f"{GE_CHEKBOX_KEY_PREFIX}gallery_checkbox"):
                    st.checkbox("Case à cocher standard", value=True, key="gallery_checkbox")
            with col2:
                with st.container(key=f"{GE_TOGGLE_KEY_PREFIX}gallery_toggle"):
                    st.toggle("Interrupteur (switch)", value=True, key="gallery_toggle")


        show_example(demo_checkbox_toggle)
        st.divider()

        # ── Modal ─────────────────────────────────────────────────────────────
        st.header("Modal", anchor="modal")
        st.write(
            "`st.dialog(...)` est un **décorateur** natif Streamlit (pas de "
            "CCv2 ici, comme les widgets ci-dessus) : on écrit une fonction, on "
            "l'appelle depuis un handler de clic, Streamlit affiche son contenu "
            "dans un overlay stylé GE-DESIGN automatiquement une fois "
            "`inject_ge_styles()` appelé, fond, coins, ombre, typographie du "
            "titre. Un seul dialog ouvert à la fois ; ESC / clic-dehors / croix de "
            "fermeture sont gérés nativement."
        )


        @st.dialog("Titre du modal")
        def _gallery_dialog():
            st.write("Contenu du dialog — n'importe quel widget Streamlit.")


        def demo_dialog():
            with st.container(key=f"{FILLED_BUTTON_KEY_PREFIX}gallery_dialog"):
                if st.button("Ouvrir le modal", key="gallery_btn_dialog"):
                    _gallery_dialog()


        show_example(demo_dialog)
        st.divider()

        # ── Alertes ───────────────────────────────────────────────────────────
        st.header("Alertes", anchor="alertes")
        st.write(
            "`st.info`/`st.success`/`st.warning`/`st.error` — stylés "
            "automatiquement une fois `inject_ge_styles()`. Habillage GE-DESIGN \"MD_Stacked card_info\""
        )


        def demo_alerts():
            st.info(
                "Uniquement les appartements non meublés en immeuble.",
                title="Périmètre de la statistique",
            )
            st.success("Analyse terminée avec succès.")
            st.warning("Vérifiez les données avant de continuer.")
            st.error("Une erreur est survenue lors du traitement.")


        show_example(demo_alerts)
        st.divider()

        # ── Typographie ───────────────────────────────────────────────────────
        st.header("Typographie", anchor="typographie")
        st.write(
            "Titres natifs Streamlit stylés automatiquement une fois "
            "`inject_ge_styles()` appelé — aucun conteneur enveloppant "
            "nécessaire. `layout.py` ajuste line-height/letter-spacing/padding "
            "sur `h1`/`h2`/`h3` directement (pas d'équivalent dans "
            "`.streamlit/config.toml` pour ce niveau de détail) : `st.title` → "
            "`h1` (typescale `headline-large`), `st.header` → `h2` (typescale "
            "`headline-small`, **partagée avec `st.subheader` → `h3`**)."
        )


        def demo_typography():
            st.title("Titre principal (st.title)")
            st.header("Titre de section (st.header)")


        show_example(demo_typography)

        st.subheader("Ligne de titre + action")
        st.write(
            "Titre de page et bouton d'action sur la MÊME ligne, bouton collé "
            "au bord droit (cf. Figma node 529:58860 et views/operations.py, "
            "qui l'utilise pour \"Importer manuellement\") — "
            "`st.container(key=\"ge-header-row\")` enveloppant un "
            "`st.columns([5, 2])` : le titre dans la 1ʳᵉ colonne, le(s) "
            "bouton(s) dans la 2ᵉ, le ratio détermine la place laissée aux "
            "boutons."
        )


        def demo_header_row():
            with st.container(key="ge-header-row"):
                title_col, action_col = st.columns([5, 2], vertical_alignment="top")
            with title_col:
                st.title("Titre de la page")
            with action_col:
                with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}gallery_header_row"):
                    st.button(
                        "Importer manuellement",
                        icon=":material/upload:",
                        key="gallery_btn_header_row",
                    )


        show_example(demo_header_row)
        st.caption(
            "Le bouton est poussé au bord droit par layout.py "
            "(`.st-key-ge-header-row [data-testid=\"stColumn\"]:last-child "
            "{ justify-content: flex-end }`) — sans cette règle, il resterait "
            "collé au bord GAUCHE de sa colonne, pas du bord droit de la page."
        )
        st.divider()

        # ── Widgets natifs stylés automatiquement ────────────────────────────
        st.header("Widgets natifs stylés automatiquement", anchor="widgets-natifs-stylés-automatiquement")
        st.write(
            "Une fois `inject_ge_styles()` appelé, ces widgets Streamlit natifs "
            "sont stylés GE-Design automatiquement — aucun conteneur "
            "enveloppant nécessaire, contrairement aux boutons et au toggle "
            "ci-dessus."
        )


        def demo_native_widgets():
            n1, n2 = st.columns(2)
            with n1:
                st.text_input("Champ texte", placeholder="Rechercher...", key="gallery_text_input")
            with n2:
                st.selectbox("Menu déroulant", options=["Tous", "Option A", "Option B"], key="gallery_selectbox")


        show_example(demo_native_widgets)
        st.caption(
            "**Non stylable** : `st.dataframe` (rendu sur `<canvas>`, pas de "
            "CSS possible — voir app.py pour le tableau des opérations, qui "
            "reste volontairement natif pour cette raison)."
        )

    with st.container(key="stepper_gallery_container"):  # slot pour le stepper sticky à droite
        ge_stepper(_GALLERY_SECTIONS)  # navigation sticky à droite, surligne la section visible
