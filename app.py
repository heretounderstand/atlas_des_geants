# ══════════════════════════════════════════════════════════════════════════
#  L'ATLAS DES GÉANTS — Forbes Global 2000 · Édition 2026
#  Un magazine de données interactif, pas un dashboard de plus.
#  Données : Kaggle (ellimaaac/forbes-the-global-2000-companies-2026)
# ══════════════════════════════════════════════════════════════════════════

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ── Configuration de la page ────────────────────────────────────────────────
st.set_page_config(
    page_title="L'Atlas des Géants · Forbes 2000 (2026)",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Identité visuelle (risographe : bleu + rouge sur papier) ────────────────
PAPER = "#F4F1E8"
PAPER_2 = "#ECE8DB"
INK = "#131318"
BLUE = "#1D3FBB"
RED = "#E8452C"
TEAL = "#0F7B6C"
GOLD = "#D99A1B"
GRID = "#D8D3C4"

RISO_SEQ = [BLUE, RED, TEAL, GOLD, "#7A4FBF", "#B23A6E", "#4A6B2A", "#8A6D3B"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Public+Sans:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    background-color: {PAPER};
    color: {INK};
    font-family: 'Public Sans', sans-serif;
}}
[data-testid="stHeader"] {{ background: {PAPER}; }}

/* ── Masthead ── */
.masthead {{
    border-top: 6px solid {INK};
    border-bottom: 2px solid {INK};
    padding: 1.1rem 0 0.9rem 0;
    margin-bottom: 0.4rem;
}}
.masthead h1 {{
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(2rem, 5vw, 3.4rem);
    line-height: 0.95;
    margin: 0;
    letter-spacing: -0.01em;
    color: {INK};
}}
.masthead h1 .bleu {{ color: {BLUE}; }}
.masthead h1 .rouge {{ color: {RED}; }}
.masthead .strap {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    color: {INK};
    display: flex; gap: 1.2rem; flex-wrap: wrap;
}}
.masthead .strap .dot {{ color: {RED}; }}

/* ── Eyebrows & titres de section ── */
.eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {RED};
    border-bottom: 1px solid {GRID};
    padding-bottom: 0.3rem;
    margin: 1.4rem 0 0.6rem 0;
}}
.section-title {{
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.55rem;
    margin: 0 0 0.4rem 0;
    color: {INK};
}}
.lede {{
    font-size: 1.02rem;
    max-width: 62ch;
    color: {INK};
}}

/* ── Cartes chiffre (façon grand livre) ── */
.ledger {{
    border: 2px solid {INK};
    background: {PAPER};
    padding: 0.9rem 1rem 0.8rem 1rem;
    box-shadow: 5px 5px 0 {BLUE}22;
    height: 100%;
}}
.ledger.rouge {{ box-shadow: 5px 5px 0 {RED}26; }}
.ledger .lab {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {INK};
    opacity: 0.75;
}}
.ledger .val {{
    font-family: 'Archivo Black', sans-serif;
    font-size: 1.9rem;
    line-height: 1.1;
    color: {BLUE};
    margin: 0.15rem 0;
}}
.ledger.rouge .val {{ color: {RED}; }}
.ledger .sub {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: {INK};
    opacity: 0.8;
}}

/* ── Encadré éditorial ── */
.callout {{
    border-left: 6px solid {RED};
    background: {PAPER_2};
    padding: 0.9rem 1.1rem;
    margin: 0.8rem 0;
    font-size: 1rem;
    max-width: 75ch;
}}
.callout b {{ color: {RED}; }}

/* ── Onglets ── */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.4rem;
    border-bottom: 2px solid {INK};
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    background: transparent;
    border: 2px solid transparent;
    border-bottom: none;
    color: {INK};
    padding: 0.45rem 0.9rem;
}}
.stTabs [aria-selected="true"] {{
    background: {INK} !important;
    color: {PAPER} !important;
    border-radius: 0;
}}

/* ── Divers ── */
[data-testid="stMetricValue"] {{ font-family: 'Archivo Black', sans-serif; }}
hr {{ border-color: {GRID}; }}
.footnote {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    opacity: 0.65;
    border-top: 1px solid {GRID};
    padding-top: 0.6rem;
    margin-top: 2rem;
}}
</style>
""", unsafe_allow_html=True)


# ── Chargement & enrichissement des données ─────────────────────────────────
AFRIQUE = {
    "South Africa": "Afrique du Sud", "Nigeria": "Nigéria", "Egypt": "Égypte",
    "Morocco": "Maroc", "Kenya": "Kenya", "Algeria": "Algérie",
    "Tunisia": "Tunisie", "Ghana": "Ghana", "Ivory Coast": "Côte d'Ivoire",
    "Senegal": "Sénégal", "Ethiopia": "Éthiopie", "Angola": "Angola",
    "Mauritius": "Maurice", "Cameroon": "Cameroun",
}

@st.cache_data
def charger():
    df = pd.read_csv("data/Forbes_2000_Companies_2026.csv", encoding="utf-8-sig")
    df = df.rename(columns={
        "Rank": "Rang", "Company": "Entreprise", "Headquarters": "Siège",
        "Industry": "Secteur", "Sales ($B)": "CA", "Profit ($B)": "Profit",
        "Assets ($B)": "Actifs", "Market Value ($B)": "Valorisation",
    })
    df["Pays"] = df["Siège"].str.rsplit(",", n=1).str[-1].str.strip()
    df["Ville"] = df["Siège"].str.rsplit(",", n=1).str[0].str.strip()
    df["Secteur"] = df["Secteur"].fillna("Non renseigné")
    df["Valorisation"] = df["Valorisation"].fillna(df["Valorisation"].median())
    # Métriques dérivées
    df["Marge nette (%)"] = (df["Profit"] / df["CA"].replace(0, np.nan) * 100).round(1)
    df["ROA (%)"] = (df["Profit"] / df["Actifs"].replace(0, np.nan) * 100).round(2)
    df["Afrique"] = df["Pays"].isin(AFRIQUE)
    return df

df = charger()

def fmt_b(x, dec=0):
    """Formate un montant en milliards de dollars."""
    if x >= 1000:
        return f"{x/1000:,.1f} T$".replace(",", " ")
    return f"{x:,.{dec}f} Md$".replace(",", " ")

def plotly_riso(fig, hauteur=460):
    """Applique l'identité visuelle aux graphiques Plotly."""
    fig.update_layout(
        paper_bgcolor=PAPER, plot_bgcolor=PAPER,
        font=dict(family="Public Sans, sans-serif", color=INK, size=13),
        colorway=RISO_SEQ, height=hauteur,
        margin=dict(l=10, r=10, t=40, b=10),
        hoverlabel=dict(font_family="IBM Plex Mono"),
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)
    return fig


# ── Masthead ────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="masthead">
  <h1>L'ATLAS <span class="bleu">DES</span> GÉANTS<span class="rouge">.</span></h1>
  <div class="strap">
    <span>Forbes Global 2000</span><span class="dot">●</span>
    <span>Édition 2026</span><span class="dot">●</span>
    <span>{df['Pays'].nunique()} pays</span><span class="dot">●</span>
    <span>{df['Secteur'].nunique()} secteurs</span><span class="dot">●</span>
    <span>Chiffres en milliards de dollars US</span>
  </div>
</div>
""", unsafe_allow_html=True)

tab_pano, tab_explo, tab_duel, tab_afrique, tab_records = st.tabs([
    "🗺️ Panorama", "🔍 Explorateur", "⚔️ Le Duel", "🌍 L'Afrique", "🏆 Records"
])


# ════════════════════════════════════════════════════════════════════════════
# 1 · PANORAMA
# ════════════════════════════════════════════════════════════════════════════
with tab_pano:
    st.markdown('<div class="eyebrow">Chapitre 01 · Vue d\'ensemble</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">2000 entreprises, une économie-monde</div>', unsafe_allow_html=True)
    st.markdown(f'<p class="lede">Le classement Forbes Global 2000 combine chiffre d\'affaires, '
                f'profits, actifs et valorisation boursière. Voici ce que pèsent, ensemble, '
                f'les 2000 plus grandes entreprises cotées de la planète en 2026.</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    kpis = [
        (c1, "Chiffre d'affaires cumulé", fmt_b(df["CA"].sum()), "≈ 2× le PIB des États-Unis", ""),
        (c2, "Profits cumulés", fmt_b(df["Profit"].sum()), "aucune entreprise en perte cette année", "rouge"),
        (c3, "Actifs cumulés", fmt_b(df["Actifs"].sum()), "dominés par le secteur bancaire", ""),
        (c4, "Valorisation cumulée", fmt_b(df["Valorisation"].sum()), f"n°1 : {df.nlargest(1,'Valorisation')['Entreprise'].iloc[0]}", "rouge"),
    ]
    for col, lab, val, sub, cls in kpis:
        col.markdown(f'<div class="ledger {cls}"><div class="lab">{lab}</div>'
                     f'<div class="val">{val}</div><div class="sub">{sub}</div></div>',
                     unsafe_allow_html=True)

    top_decile = df.nlargest(200, "Profit")["Profit"].sum() / df["Profit"].sum() * 100
    st.markdown(f'<div class="callout">Concentration extrême : les <b>200 premières entreprises '
                f'par profit</b> (10&nbsp;% du classement) captent <b>{top_decile:.0f}&nbsp;% des profits</b> '
                f'des 2000.</div>', unsafe_allow_html=True)

    g1, g2 = st.columns([3, 2])

    with g1:
        st.markdown('<div class="eyebrow">Cartographie</div>', unsafe_allow_html=True)
        metrique_tm = st.radio("Taille des blocs selon :", ["Valorisation", "Profit", "CA"],
                               horizontal=True, key="tm_metric")
        tm = df.groupby(["Pays", "Secteur"], as_index=False)[metrique_tm].sum()
        fig = px.treemap(tm, path=[px.Constant("Monde"), "Pays", "Secteur"],
                         values=metrique_tm, color_discrete_sequence=RISO_SEQ,
                         title=f"Répartition mondiale — {metrique_tm} (Md$)")
        fig.update_traces(marker=dict(cornerradius=0, line=dict(color=PAPER, width=1.5)),
                          textfont_family="IBM Plex Mono")
        st.plotly_chart(plotly_riso(fig, 520), use_container_width=True)

    with g2:
        st.markdown('<div class="eyebrow">Le poids des nations</div>', unsafe_allow_html=True)
        pays_n = df["Pays"].value_counts().head(12).reset_index()
        pays_n.columns = ["Pays", "Entreprises"]
        fig = px.bar(pays_n.sort_values("Entreprises"), x="Entreprises", y="Pays",
                     orientation="h", title="Nombre d'entreprises au classement",
                     text="Entreprises")
        fig.update_traces(marker_color=BLUE, textfont_family="IBM Plex Mono",
                          textposition="outside", cliponaxis=False)
        st.plotly_chart(plotly_riso(fig, 520), use_container_width=True)

    st.markdown('<div class="eyebrow">Les secteurs</div>', unsafe_allow_html=True)
    sect = df.groupby("Secteur", as_index=False).agg(
        Entreprises=("Entreprise", "count"), Profit=("Profit", "sum"),
        CA=("CA", "sum"), Marge=("Marge nette (%)", "median"))
    fig = px.scatter(sect, x="CA", y="Profit", size="Entreprises", color="Marge",
                     hover_name="Secteur", size_max=52, log_x=True, log_y=True,
                     color_continuous_scale=[[0, BLUE], [0.5, GOLD], [1, RED]],
                     labels={"CA": "CA cumulé (Md$, échelle log)",
                             "Profit": "Profit cumulé (Md$, échelle log)",
                             "Marge": "Marge médiane (%)"},
                     title="27 secteurs : volume d'affaires vs profits (taille = nombre d'entreprises)")
    st.plotly_chart(plotly_riso(fig, 480), use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# 2 · EXPLORATEUR
# ════════════════════════════════════════════════════════════════════════════
with tab_explo:
    st.markdown('<div class="eyebrow">Chapitre 02 · À vous de jouer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Explorateur du classement</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns([2, 2, 3])
    pays_sel = f1.multiselect("Pays", sorted(df["Pays"].unique()), placeholder="Tous les pays")
    sect_sel = f2.multiselect("Secteurs", sorted(df["Secteur"].unique()), placeholder="Tous les secteurs")
    rang_max = f3.slider("Profondeur du classement (rang max)", 10, 2000, 2000, step=10)

    dff = df[df["Rang"] <= rang_max]
    if pays_sel:
        dff = dff[dff["Pays"].isin(pays_sel)]
    if sect_sel:
        dff = dff[dff["Secteur"].isin(sect_sel)]

    if dff.empty:
        st.warning("Aucune entreprise ne correspond à ces filtres. Élargissez la sélection.")
    else:
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Entreprises", f"{len(dff):,}".replace(",", " "))
        k2.metric("CA cumulé", fmt_b(dff["CA"].sum()))
        k3.metric("Profit cumulé", fmt_b(dff["Profit"].sum(), 1))
        k4.metric("Marge nette médiane", f"{dff['Marge nette (%)'].median():.1f} %")

        st.markdown('<div class="eyebrow">Nuage des géants</div>', unsafe_allow_html=True)
        fig = px.scatter(
            dff, x="CA", y="Profit", size="Valorisation", color="Secteur",
            hover_name="Entreprise", log_x=True, log_y=True, size_max=44,
            hover_data={"Rang": True, "Pays": True, "Marge nette (%)": True,
                        "CA": ":.1f", "Profit": ":.1f", "Valorisation": ":.0f"},
            labels={"CA": "Chiffre d'affaires (Md$, log)", "Profit": "Profit (Md$, log)"},
            title="Chaque bulle est une entreprise · taille = valorisation boursière")
        st.plotly_chart(plotly_riso(fig, 560), use_container_width=True)

        st.markdown('<div class="eyebrow">Le grand livre</div>', unsafe_allow_html=True)
        recherche = st.text_input("Rechercher une entreprise", placeholder="Ex. : MTN, Toyota, Attijariwafa…")
        table = dff if not recherche else dff[dff["Entreprise"].str.contains(recherche, case=False, na=False)]
        st.dataframe(
            table[["Rang", "Entreprise", "Pays", "Secteur", "CA", "Profit",
                   "Actifs", "Valorisation", "Marge nette (%)", "ROA (%)"]]
            .sort_values("Rang").set_index("Rang"),
            use_container_width=True, height=420,
            column_config={
                "CA": st.column_config.NumberColumn("CA (Md$)", format="%.1f"),
                "Profit": st.column_config.NumberColumn("Profit (Md$)", format="%.2f"),
                "Actifs": st.column_config.NumberColumn("Actifs (Md$)", format="%.0f"),
                "Valorisation": st.column_config.NumberColumn("Valorisation (Md$)", format="%.0f"),
            })
        st.download_button("⬇ Exporter la sélection (CSV)",
                           table.to_csv(index=False).encode("utf-8"),
                           "atlas_selection.csv", "text/csv")


# ════════════════════════════════════════════════════════════════════════════
# 3 · LE DUEL
# ════════════════════════════════════════════════════════════════════════════
with tab_duel:
    st.markdown('<div class="eyebrow">Chapitre 03 · Face à face</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Le Duel</div>', unsafe_allow_html=True)
    st.markdown('<p class="lede">Deux entreprises entrent, les chiffres tranchent. '
                'Comparez n\'importe quelle paire du classement — y compris David contre Goliath.</p>',
                unsafe_allow_html=True)

    entreprises = df.sort_values("Rang")["Entreprise"].tolist()
    d1, dvs, d2 = st.columns([5, 1, 5])
    a = d1.selectbox("🔵 Dans le coin bleu", entreprises, index=entreprises.index("Apple") if "Apple" in entreprises else 0)
    dvs.markdown("<div style='text-align:center;font-family:Archivo Black;font-size:2rem;padding-top:1.6rem;'>VS</div>", unsafe_allow_html=True)
    b = d2.selectbox("🔴 Dans le coin rouge", entreprises,
                     index=entreprises.index("MTN Group") if "MTN Group" in entreprises else 1)

    if a == b:
        st.info("Choisissez deux entreprises différentes pour lancer le duel.")
    else:
        ra, rb = df[df["Entreprise"] == a].iloc[0], df[df["Entreprise"] == b].iloc[0]

        ca_, cb_ = st.columns(2)
        for col, r, cls in [(ca_, ra, ""), (cb_, rb, "rouge")]:
            col.markdown(
                f'<div class="ledger {cls}"><div class="lab">Rang mondial n°{r["Rang"]} · {r["Pays"]}</div>'
                f'<div class="val">{r["Entreprise"]}</div>'
                f'<div class="sub">{r["Secteur"]} — {r["Ville"]}</div></div>',
                unsafe_allow_html=True)

        st.write("")
        indicateurs = ["CA", "Profit", "Actifs", "Valorisation"]
        fig = go.Figure()
        fig.add_bar(name=a, y=indicateurs, x=[ra[i] for i in indicateurs],
                    orientation="h", marker_color=BLUE,
                    text=[fmt_b(ra[i], 1) for i in indicateurs], textfont_family="IBM Plex Mono")
        fig.add_bar(name=b, y=indicateurs, x=[rb[i] for i in indicateurs],
                    orientation="h", marker_color=RED,
                    text=[fmt_b(rb[i], 1) for i in indicateurs], textfont_family="IBM Plex Mono")
        fig.update_layout(barmode="group", title="Les quatre piliers du classement Forbes (Md$)",
                          xaxis_type="log")
        st.plotly_chart(plotly_riso(fig, 420), use_container_width=True)

        st.markdown('<div class="eyebrow">À armes égales — les ratios</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        duels_ratio = [
            (r1, "Marge nette", ra["Marge nette (%)"], rb["Marge nette (%)"], "%"),
            (r2, "ROA (profit / actifs)", ra["ROA (%)"], rb["ROA (%)"], "%"),
            (r3, "Valorisation / CA", ra["Valorisation"] / ra["CA"], rb["Valorisation"] / rb["CA"], "×"),
        ]
        for col, lab, va, vb, u in duels_ratio:
            gagnant = a if va >= vb else b
            couleur = BLUE if va >= vb else RED
            col.markdown(
                f'<div class="ledger"><div class="lab">{lab}</div>'
                f'<div class="val" style="font-size:1.2rem;color:{INK}">'
                f'<span style="color:{BLUE}">{va:.1f}{u}</span> · '
                f'<span style="color:{RED}">{vb:.1f}{u}</span></div>'
                f'<div class="sub">avantage <b style="color:{couleur}">{gagnant}</b></div></div>',
                unsafe_allow_html=True)

        ecart = max(ra["Valorisation"], rb["Valorisation"]) / max(min(ra["Valorisation"], rb["Valorisation"]), 0.01)
        if ecart >= 3:
            grand = a if ra["Valorisation"] > rb["Valorisation"] else b
            petit = b if grand == a else a
            st.markdown(f'<div class="callout">En Bourse, <b>{grand}</b> vaut environ '
                        f'<b>{ecart:,.0f} fois</b> {petit}. Le classement Forbes, lui, pondère aussi '
                        f'CA, profits et actifs — d\'où des rangs parfois surprenants.</div>'.replace(",", " "),
                        unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# 4 · L'AFRIQUE — le chapitre signature
# ════════════════════════════════════════════════════════════════════════════
with tab_afrique:
    afr = df[df["Afrique"]].copy()
    afr["Pays FR"] = afr["Pays"].map(AFRIQUE)
    nvidia_mv = float(df.loc[df["Entreprise"] == "NVIDIA", "Valorisation"].iloc[0]) if (df["Entreprise"] == "NVIDIA").any() else None

    st.markdown('<div class="eyebrow">Chapitre 04 · L\'angle qui nous concerne</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">L\'Afrique dans le top 2000 mondial</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    donnees = [
        (c1, "Entreprises africaines", f"{len(afr)} / 2000", f"soit {len(afr)/20:.1f} % du classement", "rouge"),
        (c2, "Pays représentés", f"{afr['Pays'].nunique()}", " · ".join(sorted(afr["Pays FR"].unique())), ""),
        (c3, "Meilleure position", f"n°{int(afr['Rang'].min())}", afr.nsmallest(1, "Rang")["Entreprise"].iloc[0], ""),
        (c4, "Valorisation cumulée", fmt_b(afr["Valorisation"].sum()), "pour les "
         f"{len(afr)} entreprises réunies", "rouge"),
    ]
    for col, lab, val, sub, cls in donnees:
        col.markdown(f'<div class="ledger {cls}"><div class="lab">{lab}</div>'
                     f'<div class="val">{val}</div><div class="sub">{sub}</div></div>',
                     unsafe_allow_html=True)

    if nvidia_mv:
        ratio = nvidia_mv / afr["Valorisation"].sum()
        st.markdown(f'<div class="callout">Mise en perspective : <b>NVIDIA seule</b> '
                    f'({fmt_b(nvidia_mv)}) pèse en Bourse <b>{ratio:.0f} fois</b> les '
                    f'{len(afr)} entreprises africaines du classement réunies '
                    f'({fmt_b(afr["Valorisation"].sum())}). Le continent représente ~18&nbsp;% de '
                    f'l\'humanité et {len(afr)/20:.1f}&nbsp;% de ce classement — l\'écart est '
                    f'l\'opportunité.</div>', unsafe_allow_html=True)

    ga, gb = st.columns([3, 2])
    with ga:
        st.markdown('<div class="eyebrow">Les 17 sur la ligne du classement</div>', unsafe_allow_html=True)
        fig = px.scatter(afr.sort_values("Rang"), x="Rang", y="Valorisation",
                         color="Pays FR", size="Profit", hover_name="Entreprise",
                         size_max=30, text="Entreprise",
                         hover_data={"Secteur": True, "CA": ":.1f", "Profit": ":.2f"},
                         labels={"Valorisation": "Valorisation (Md$)", "Pays FR": "Pays"},
                         title="Position au classement mondial (plus à gauche = mieux classé)")
        fig.update_traces(textposition="top center", textfont=dict(family="IBM Plex Mono", size=9))
        fig.update_xaxes(autorange="reversed")
        st.plotly_chart(plotly_riso(fig, 500), use_container_width=True)

    with gb:
        st.markdown('<div class="eyebrow">Répartition sectorielle</div>', unsafe_allow_html=True)
        sect_afr = afr["Secteur"].value_counts().reset_index()
        sect_afr.columns = ["Secteur", "Entreprises"]
        fig = px.bar(sect_afr.sort_values("Entreprises"), x="Entreprises", y="Secteur",
                     orientation="h", text="Entreprises",
                     title="La finance domine largement")
        fig.update_traces(marker_color=RED, textfont_family="IBM Plex Mono",
                          textposition="outside", cliponaxis=False)
        st.plotly_chart(plotly_riso(fig, 500), use_container_width=True)

    st.markdown('<div class="eyebrow">Le tableau d\'honneur</div>', unsafe_allow_html=True)
    st.dataframe(
        afr[["Rang", "Entreprise", "Pays FR", "Secteur", "CA", "Profit", "Valorisation", "Marge nette (%)"]]
        .sort_values("Rang").rename(columns={"Pays FR": "Pays"}).set_index("Rang"),
        use_container_width=True,
        column_config={
            "CA": st.column_config.NumberColumn("CA (Md$)", format="%.2f"),
            "Profit": st.column_config.NumberColumn("Profit (Md$)", format="%.2f"),
            "Valorisation": st.column_config.NumberColumn("Valorisation (Md$)", format="%.1f"),
        })


# ════════════════════════════════════════════════════════════════════════════
# 5 · RECORDS
# ════════════════════════════════════════════════════════════════════════════
with tab_records:
    st.markdown('<div class="eyebrow">Chapitre 05 · Superlatifs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Le livre des records 2026</div>', unsafe_allow_html=True)

    solide = df[df["CA"] > 10]  # éviter les artefacts de petites bases
    records = [
        ("💰 Le plus gros profit", *df.nlargest(1, "Profit")[["Entreprise", "Profit"]].iloc[0],
         "Md$ de bénéfice net"),
        ("📈 La plus grosse valorisation", *df.nlargest(1, "Valorisation")[["Entreprise", "Valorisation"]].iloc[0],
         "Md$ en Bourse"),
        ("🏦 Le plus d'actifs", *df.nlargest(1, "Actifs")[["Entreprise", "Actifs"]].iloc[0],
         "Md$ d'actifs au bilan"),
        ("🛒 Le plus gros CA", *df.nlargest(1, "CA")[["Entreprise", "CA"]].iloc[0],
         "Md$ de chiffre d'affaires"),
        ("🎯 La meilleure marge*", *solide.nlargest(1, "Marge nette (%)")[["Entreprise", "Marge nette (%)"]].iloc[0],
         "% de marge nette"),
        ("⚡ Le meilleur ROA*", *solide.nlargest(1, "ROA (%)")[["Entreprise", "ROA (%)"]].iloc[0],
         "% de rendement des actifs"),
    ]
    cols = st.columns(3)
    for i, (titre, nom, valeur, unite) in enumerate(records):
        cls = "rouge" if i % 2 else ""
        cols[i % 3].markdown(
            f'<div class="ledger {cls}" style="margin-bottom:0.9rem;">'
            f'<div class="lab">{titre}</div><div class="val" style="font-size:1.35rem;">{nom}</div>'
            f'<div class="sub">{valeur:,.1f} {unite}</div></div>'.replace(",", " "),
            unsafe_allow_html=True)

    st.caption("*parmi les entreprises réalisant plus de 10 Md$ de chiffre d'affaires.")

    st.markdown('<div class="eyebrow">La courbe de la concentration</div>', unsafe_allow_html=True)
    tri = df.sort_values("Profit", ascending=False).reset_index(drop=True)
    tri["Part cumulée des profits (%)"] = tri["Profit"].cumsum() / tri["Profit"].sum() * 100
    tri["Part des entreprises (%)"] = (tri.index + 1) / len(tri) * 100
    fig = px.area(tri, x="Part des entreprises (%)", y="Part cumulée des profits (%)",
                  title="Quelle part des entreprises capte quelle part des profits ?")
    fig.update_traces(line_color=BLUE, fillcolor=f"rgba(29,63,187,0.12)")
    fig.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                  line=dict(color=RED, dash="dash", width=2))
    fig.add_annotation(x=62, y=58, text="Égalité parfaite", font=dict(color=RED, family="IBM Plex Mono", size=11),
                       showarrow=False, textangle=-15)
    st.plotly_chart(plotly_riso(fig, 440), use_container_width=True)


# ── Pied de page ─────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footnote">L\'ATLAS DES GÉANTS · données : Forbes Global 2000 (2026), '
    'via Kaggle (ellimaaac) · montants en milliards de dollars US · '
    'app Streamlit + Plotly · un projet de la série « Évolution »</div>',
    unsafe_allow_html=True)
