# GE-DESIGN-KIT pour Streamlit

Composants réutilisables pour habiller une app Streamlit aux couleurs et à la typographie **GE-DESIGN**.

---

## Installation

```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Le kit n'est pas un package pip, copier le dossier `ge_design_kit/`, `assets/` et `.streamlit/config.toml` tels quels à la racine du projet, à côté du fichier `app.py`.

⚠️ Nécessite une version **récente** de Streamlit (Custom Components v2). En cas d'erreur liée à `st.components.v2` : `pip install --upgrade streamlit`.

---

## Lancer l'application

```bash
streamlit run app.py --server.port 8501
```

---

## Galerie de composants

```bash
streamlit run gallery.py --server.port 8502
```

Outil de développement autonome (pas une page de l'app) : rendu réel
de chaque composant du kit **+ le code Python exact qui l'a produit**
sous chaque exemple, pour démarrer rapidement sans relire tout ce
README. Voir `gallery.py`.

---

## Démarrage rapide

```python
import streamlit as st
from ge_design_kit import inject_ge_styles, ge_topbar, TOPBAR_SLOT_KEY

st.set_page_config(page_title="Mon app", layout="wide")

inject_ge_styles()  # polices + tokens + CSS, 1 seul appel, tout en haut

with st.container(key=TOPBAR_SLOT_KEY):
    ge_topbar(app_name="GE", user_label="Mon compte")

st.logo("assets/mon_logo.svg", size="small")
```

À partir de là : composants `ge_*` et widgets Streamlit natifs (`st.text_input`, `st.selectbox`, `st.button`, `st.toggle`) sont stylés GE-DESIGN automatiquement. Voir `app.py` pour un exemple complet et fonctionnel (sidebar, breadcrumb, cartes, tableau, filtres).

**`.streamlit/config.toml` est obligatoire**, sans lui, les composants `ge_*` restent stylés mais les widgets natifs (titres, boutons...) gardent l'apparence Streamlit par défaut.

---

## Composants

| Composant | Rôle | Paramètres clés | Retour |
|---|---|---|---|
| `inject_ge_styles()` | Charge tout (polices/tokens/layout). À appeler 1x, tout en haut. | - | - |
| `ge_topbar(app_name, user_label)` | Bandeau institutionnel fixe en haut. À wrapper dans `st.container(key=TOPBAR_SLOT_KEY)`. | `app_name="GE"`, `user_label="Mon compte"` | - |
| `ge_sidebar(items, title, active_id, key)` | Menu latéral. À utiliser dans `with st.sidebar:`. | `items`: `[{"id","label","icon","has_children"?}]` ou `{"divider":True}` | id cliqué ou `None` |
| `ge_breadcrumb(items, key)` | Fil d'Ariane, dernier item = page courante (non cliquable). | `items`: `[{"id","label"}]` | id cliqué ou `None` |
| `ge_surface(key, variant)` | Conteneur de page, peut contenir n'importe quel widget (contrairement à `ge_card`). | `variant="card"` (blanc+ombre) ou `"inset"` (teinté, sans ombre) | context manager |
| `ge_card(title, content, icon, button_label, key)` | Card figée (titre+texte+bouton). Composant CCv2, ne peut pas contenir d'autres widgets. | tous optionnels sauf `title`/`content` | `True` si bouton cliqué |
| `ge_kpi(value, label, key)` | KPI card simple, sans interaction. | tous requis | - |

Icônes : nom **Material Symbols** (ex: `"search"`), pas d'emoji — liste sur [fonts.google.com/icons](https://fonts.google.com/icons).

Détails complets de chaque fonction (docstrings) directement dans le code source de `ge_design_kit/`.

---

## Boutons

`st.button()` n'accepte pas de classe CSS personnalisée, le style passe donc par un **conteneur enveloppant**, pas par le bouton lui-même. Trois variantes, vocabulaire Material Design 3 (déjà utilisé partout ailleurs dans le kit) :

```python
from ge_design_kit import FILLED_BUTTON_KEY_PREFIX, OUTLINED_BUTTON_KEY_PREFIX, TEXT_BUTTON_KEY_PREFIX

with st.container(key=f"{OUTLINED_BUTTON_KEY_PREFIX}mon_bouton"):
    if st.button("Importer manuellement", icon=":material/upload:", key="btn_import"):
        ...
```

| Variante | Rendu | Usage typique |
|---|---|---|
| `FILLED_BUTTON_KEY_PREFIX` | Fond `primary` plein | Bouton icône seule (ex: recherche) |
| `OUTLINED_BUTTON_KEY_PREFIX` | Contour fin, fond transparent | Action secondaire (ex: "Importer", "Comparer") |
| `TEXT_BUTTON_KEY_PREFIX` | Pas de bordure ni de fond, libellé coloré | Action discrète (ex: "Annuler la sélection") |

`ge_label_spacer(height_px=10)` - aligne un bouton (sans label au-dessus) avec des champs voisins qui, eux, en affichent un (`text_input`, `selectbox`...).

⚠️ `ICON_BUTTON_KEY_PREFIX` / `PILL_BUTTON_KEY_PREFIX` existent encore comme alias de `FILLED_`/`OUTLINED_BUTTON_KEY_PREFIX` (ancien nommage), à préférer les noms `FILLED_`/`OUTLINED_`/`TEXT_` dans tout nouveau code.

---

## Widgets natifs stylés automatiquement

Une fois `inject_ge_styles()` appelé : `st.text_input`, `st.selectbox`, `st.toggle`, `st.button`/`st.form_submit_button` (types `"secondary"`/`"tertiary"`, cf. section Boutons ci-dessus), titres (`st.title`, `#`/`##`/`###`).

**Non stylable** : `st.dataframe` (rendu sur `<canvas>`, pas de CSS possible.

---

## Pièges à connaître (pour étendre le kit)

- **Jamais de `<balise>` littérale dans un commentaire CSS** , tout passe par `st.html()` → DOMPurify, qui peut interpréter le contenu d'un commentaire comme du vrai HTML et casser tout le CSS qui suit.
- **`st.markdown(unsafe_allow_html=True)` casse sur les lignes vides** , préférer `st.html()` pour du CSS/HTML multi-lignes.
- **Ne jamais cibler les classes `st-emotion-cache-*`** (instables, régénérées à chaque build) , chercher un `data-testid` ou un rôle ARIA stable à la place.
- **`st.container(key="...")`** génère une classe `.st-key-<key>` , le moyen fiable de cibler un élément précis en CSS.
- **`height:100%` casse si un seul niveau de la chaîne de parents n'a pas de hauteur définie** , Streamlit imbrique beaucoup de wrappers ; en cas de doute, préférer une hauteur fixe calibrée visuellement.
- **On ne peut pas modifier `st.session_state[key]` après instanciation du widget dans le run courant.** Pour un reset ponctuel, poser un drapeau et l'appliquer au début du run suivant peut suffire, mais ce n'est pas fiable pour des resets répétés (fonctionne la première fois, pas forcément les suivantes, comportement interne de Streamlit non documenté). La solution robuste : rendre la `key` du widget dynamique (ex: un compteur incrémenté à chaque reset, `key=f"mon_widget_{compteur}"`). Changer la `key` force Streamlit à traiter le widget comme entièrement nouveau, sans aucun état résiduel possible.
- **Un bouton dans un conteneur flex peut se faire comprimer** (texte qui passe à la ligne) si son conteneur n'a pas `flex-shrink: 0` , toujours l'ajouter explicitement sur les boutons custom.
- **`:hover` s'applique aussi aux boutons `disabled` par défaut** , utiliser `:not(:disabled):hover` pour l'exclure.

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/
```

Un seul test pour l'instant: `tests/test_data_testid_smoke.py`. Le kit
style les widgets natifs Streamlit via des sélecteurs `[data-testid="..."]`
(cf. Pièges à connaître ci-dessus), une convention interne à Streamlit,
pas une API publique, qui peut changer de nom d'une version à l'autre
sans erreur ni changelog (déjà arrivé : `stLogo` est devenu
`stSidebarLogo`/`stHeaderLogo`, et le topbar s'est mis à se faire
chevaucher silencieusement par le logo, sans qu'aucune exception ne
soit levée nulle part). Ce test grep le bundle JS de Streamlit
installé pour vérifier que chaque `data-testid` dont le kit dépend
existe encore, sans navigateur, en ~0.3s — pour transformer un futur
renommage silencieux en échec de test immédiat plutôt qu'en régression
visuelle découverte par hasard.

---

## Ressources

[Docs Streamlit](https://docs.streamlit.io) · [Custom Components v2](https://docs.streamlit.io/develop/concepts/custom-components/components-v2) · [Material Symbols](https://fonts.google.com/icons)