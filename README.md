# 🗺️ L'Atlas des Géants

Un magazine de données interactif construit sur le classement **Forbes Global 2000 — Édition 2026**. Plutôt qu'un dashboard générique, l'app raconte le classement en cinq chapitres, avec une identité risographe (bleu/rouge sur papier) et un chapitre signature consacré à la place de l'Afrique dans le top 2000 mondial.

## Les cinq chapitres

1. **Panorama** — KPI cumulés, treemap monde → pays → secteur, poids des nations, cartographie des 27 secteurs.
2. **Explorateur** — filtres pays/secteur/profondeur, nuage de bulles CA × Profit × Valorisation, table consultable et export CSV.
3. **Le Duel** — comparateur tête-à-tête de deux entreprises quelconques, avec ratios « à armes égales » (marge nette, ROA, valorisation/CA).
4. **L'Afrique** — 17 entreprises sur 2000 : qui, où, dans quels secteurs, et la mise en perspective (NVIDIA vaut ~20× toutes les entreprises africaines du classement réunies).
5. **Records** — superlatifs du millésime et courbe de concentration des profits.

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud (gratuit)

1. Pousser ce dossier sur un dépôt GitHub public (`app.py`, `data/`, `requirements.txt`, `.streamlit/`).
2. Sur [share.streamlit.io](https://share.streamlit.io), « New app » → sélectionner le dépôt, branche `main`, fichier `app.py`.
3. Déployer. L'URL sera du type `https://<nom>.streamlit.app`.

## Données

- Source : [Forbes Global 2000 Companies 2026 (Kaggle, ellimaaac)](https://www.kaggle.com/datasets/ellimaaac/forbes-the-global-2000-companies-2026)
- 2000 lignes · 8 colonnes · montants en milliards de dollars US.
- Enrichissements calculés au chargement : pays/ville extraits du siège, marge nette, ROA, drapeau Afrique.

## Stack

Streamlit · Pandas · Plotly · CSS custom (Archivo Black / Public Sans / IBM Plex Mono).
