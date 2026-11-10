import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# ------------------------------------------------------------------
# Configuration et palette
# ------------------------------------------------------------------
AUTHOR = "AZIZI SALMA"
st.set_page_config(
    page_title="CO₂ Analyst · " + AUTHOR, 
    page_icon="", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Palette Moderne Claire & Pro
BG = "#F8FAFC"          # Fond gris très clair (confortable pour les yeux)
SURFACE = "#FFFFFF"     # Blanc pur pour les éléments
LINE = "#E2E8F0"        # Bordures subtiles
TEXT = "#0F172A"        # Texte principal (presque noir, très lisible)
MUTED = "#64748B"       # Texte secondaire élégant

# Couleurs d'accentuation modernes
PRIMARY = "#3B82F6"     # Bleu professionnel moderne
SECONDARY = "#F97316"   # Orange doux pour les highlights
ACCENT = "#10B981"      # Vert émeraude pour les succès/données positives
SEQ = [PRIMARY, SECONDARY, ACCENT, "#8B5CF6", "#EC4899", "#64748B", "#0EA5E9", "#EAB308"]
HEAT = ["#DBEAFE", "#93C5FD", "#F97316", "#EA580C"] 

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Base */
html, body, [class*="css"], .stApp {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    color: {TEXT}; 
    background-color: {BG} !important;
}}

/* Header & Footer Clean */
#MainMenu, footer {{ visibility: hidden; }} 
header[data-testid="stHeader"] {{ background: transparent; }}

.block-container {{ padding-top: 2.5rem; max-width: 1400px; margin: 0 auto; }}

/* Typographie Moderne */
h1, h2, h3 {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    color: {TEXT}; 
    font-weight: 700; 
    letter-spacing: -0.03em; 
}}

/* --- SIDEBAR MODERNE & PRO --- */
[data-testid="stSidebar"] {{ 
    background: {SURFACE} !important; 
    border-right: 1px solid {LINE} !important; 
    box-shadow: 4px 0 24px rgba(0,0,0,0.02) !important;
    z-index: 100;
}}
[data-testid="stSidebar"] * {{ color: {TEXT}; }}

.brand {{ 
    background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
    border: 1px solid {LINE}; 
    border-radius: 16px; 
    padding: 24px 20px; 
    margin-bottom: 32px; 
    text-align: center;
}}
.brand .app {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    font-weight: 800; 
    font-size: 1.6rem; 
    color: {TEXT};
    background: -webkit-linear-gradient(45deg, {PRIMARY}, {SECONDARY});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    letter-spacing: -0.02em;
}}
.brand .by {{ color: {MUTED}; font-size: .85rem; line-height: 1.5; font-weight: 500; }}
.brand .name {{ font-weight: 700; letter-spacing: .02em; color: {PRIMARY}; }}

.side-title {{ 
    color: {MUTED}; 
    font-size: .7rem; 
    font-weight: 700; 
    text-transform: uppercase; 
    letter-spacing: 0.1em; 
    margin: 28px 0 12px 8px; 
    opacity: 0.9;
}}

/* Boutons Sidebar Élégants */
[data-testid="stSidebar"] .stButton > button {{
    width: 100%; 
    justify-content: flex-start; 
    border-radius: 12px; 
    border: 1px solid transparent; 
    background: transparent; 
    color: {TEXT}; 
    font-weight: 600;
    font-size: 0.95rem;
    padding: 12px 18px;
    margin-bottom: 6px;
    transition: all .2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: none;
}}

[data-testid="stSidebar"] .stButton > button:hover {{ 
    background: #F1F5F9; 
    color: {PRIMARY}; 
    transform: translateX(4px);
}}

/* Bouton Actif (Primary) */
[data-testid="stSidebar"] .stButton > button[kind="primary"], 
[data-testid="stSidebar"] button[data-testid="stBaseButton-primary"] {{ 
    background: {PRIMARY} !important; 
    border-color: {PRIMARY} !important; 
    color: #fff !important; 
    font-weight: 600 !important; 
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
}}

[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {{ 
    background: #2563EB !important; 
    border-color: #2563EB !important; 
    transform: translateX(0);
    box-shadow: 0 6px 16px rgba(59, 130, 246, 0.3);
}}

/* Boutons secondaires (Maghreb, Géants...) */
[data-testid="stSidebar"] .row-widget.stButton > button {{
    font-size: 0.8rem;
    padding: 8px 12px;
    justify-content: center;
    border: 1px solid {LINE};
    background: #F8FAFC;
    border-radius: 8px;
    font-weight: 500;
}}
[data-testid="stSidebar"] .row-widget.stButton > button:hover {{
    background: #fff;
    border-color: {PRIMARY};
    color: {PRIMARY};
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}

/* Main Content Styles */
.topbar {{ display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }}
.pill {{ 
    border: 1px solid {LINE}; 
    background: {SURFACE}; 
    border-radius: 999px; 
    padding: 8px 18px; 
    font-size: .85rem; 
    color: {MUTED}; 
    font-weight: 600;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}}
.pill b {{ color: {SECONDARY}; font-weight: 700; }}

.page-title {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    font-weight: 800; 
    font-size: clamp(2.2rem, 5vw, 3.2rem); 
    letter-spacing: -0.04em; 
    margin: 12px 0 8px 0; 
    color: {TEXT};
}}
.page-sub {{ color: {MUTED}; max-width: 70ch; margin-bottom: 32px; font-size: 1.15rem; line-height: 1.6; font-weight: 400; }}

/* Hero Section */
.hero-label {{ color: {MUTED}; margin: 0 0 .8rem 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.85rem; }}
.hero-number {{ 
    font-family: 'Plus Jakarta Sans', sans-serif; 
    font-weight: 800; 
    font-size: clamp(4rem, 10vw, 8rem); 
    line-height: 1; 
    letter-spacing: -0.05em; 
    color: {TEXT}; 
    margin-bottom: 10px;
}}
.hero-unit {{ font-size: 1.8rem; color: {SECONDARY}; font-weight: 600; margin-left: .8rem; letter-spacing: 0; vertical-align: middle; }}

/* Cartes KPI Modernes */
.kpi {{ 
    background: {SURFACE}; 
    border: 1px solid {LINE}; 
    border-radius: 20px; 
    padding: 24px 28px; 
    height: 100%; 
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.kpi:hover {{ 
    transform: translateY(-4px); 
    box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.06); 
    border-color: #CBD5E1;
}}
.kpi .k {{ color: {MUTED}; font-size: .9rem; font-weight: 600; margin-bottom: 8px; }}
.kpi .v {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; font-weight: 800; color: {TEXT}; letter-spacing: -0.02em; }}
.kpi .n {{ color: {MUTED}; font-size: .85rem; margin-top: 6px; font-weight: 500; }}

/* Explications et Insights */
.explain {{ 
    background: #EFF6FF; 
    border: 1px solid #BFDBFE; 
    border-radius: 16px; 
    padding: 20px 24px; 
    margin-bottom: 24px; 
    line-height: 1.7; 
    color: #1E40AF;
    font-size: 0.95rem;
}}
.explain b {{ color: #1D4ED8; }}

.insight {{ 
    border-left: 4px solid {SECONDARY}; 
    background: #FFF7ED; 
    padding: 20px 24px; 
    border-radius: 0 16px 16px 0; 
    margin: 20px 0; 
    line-height: 1.7; 
    color: #9A3412;
    font-size: 0.95rem;
}}

.foot {{ color: {MUTED}; font-size: .9rem; margin-top: 60px; text-align: center; opacity: 0.8; font-weight: 500; }}
.foot b {{ color: {TEXT}; font-weight: 700; }}

[data-testid="stExpander"] {{ 
    border: 1px solid {LINE}; 
    border-radius: 12px; 
    background: transparent; 
    margin-bottom: 12px;
}}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Chargement des données…")
def load_data():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    d = pd.read_csv(url)
    d = d[d["iso_code"].str.fullmatch(r"[A-Z]{3}", na=False)]
    return d[d["year"] >= 1950].copy()


try:
    df = load_data()
except Exception as e:
    st.error(f"Impossible de charger les données : {e}. Vérifiez la connexion puis rechargez la page.")
    st.stop()

LABELS = {"co2_per_capita": "CO₂ par habitant (t)", "co2": "CO₂ total (Mt)", "cumulative_co2": "CO₂ cumulé (Mt)"}
countries_all = sorted(df["country"].unique())
DEFAULT_PICK = ["Morocco", "France", "China", "United States"]


def fmt(x):
    return f"{x:,.0f}".replace(",", " ")


def style(fig, h=440):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans", color=TEXT), 
        height=h, 
        margin=dict(l=10, r=10, t=30, b=10),
        legend_title_text="", 
        hoverlabel=dict(bgcolor=SURFACE, font_size=13, font_color=TEXT, bordercolor=LINE),
    )
    fig.update_xaxes(gridcolor=LINE, zeroline=False, showgrid=True)
    fig.update_yaxes(gridcolor=LINE, zeroline=False, showgrid=True)
    return fig


def kpi(label, value, note=""):
    return f'<div class="kpi"><div class="k">{label}</div><div class="v">{value}</div><div class="n">{note}</div></div>'


def explain(title, body):
    st.markdown(f'<div class="explain"><b>{title}</b><br>{body}</div>', unsafe_allow_html=True)


def insight(text):
    st.markdown(f'<div class="insight">{text}</div>', unsafe_allow_html=True)


PAGES = {
    "Vue d’ensemble": ":material/dashboard:",
    "Classement": ":material/leaderboard:",
    "Évolution": ":material/show_chart:",
    "Carte du monde": ":material/public:",
    "PIB et CO₂": ":material/payments:",
    "Guide et méthode": ":material/menu_book:",
}
st.session_state.setdefault("page", "Vue d’ensemble")
st.session_state.setdefault("picked", [c for c in DEFAULT_PICK if c in countries_all])


def go(p):
    st.session_state.page = p


def preset(names):
    st.session_state.picked = [c for c in names if c in countries_all]


# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f'<div class="brand"><div class="app"> CO₂ Analyst</div>'
        f'<div class="by">Projet réalisé par<br><span class="name">{AUTHOR}</span></div></div>',
        unsafe_allow_html=True,
    )
    
    st.markdown('<div class="side-title">Navigation</div>', unsafe_allow_html=True)
    for name, icon in PAGES.items():
        st.button(name, icon=icon, key=f"nav_{name}", on_click=go, args=(name,),
                  type="primary" if st.session_state.page == name else "secondary")

    st.markdown('<div class="side-title">Année analysée</div>', unsafe_allow_html=True)
    min_y, max_y = int(df["year"].min()), int(df["year"].max())
    year = st.slider("Année", min_y, max_y, min(2022, max_y), label_visibility="collapsed")

    st.markdown('<div class="side-title">Pays à comparer</div>', unsafe_allow_html=True)
    st.multiselect("Pays", countries_all, key="picked", label_visibility="collapsed")
    
    b1, b2, b3 = st.columns(3)
    b1.button("Maghreb", key="p1", on_click=preset, args=(["Morocco", "Algeria", "Tunisia", "Egypt"],))
    b2.button("Géants", key="p2", on_click=preset, args=(["China", "United States", "India", "Russia"],))
    b3.button("Europe", key="p3", on_click=preset, args=(["France", "Germany", "Italy", "Spain"],))
    
    st.button("Réinitialiser", icon=":material/restart_alt:", key="p4", on_click=preset, args=(DEFAULT_PICK,))

    st.markdown('<div class="side-title">Exporter</div>', unsafe_allow_html=True)
    picked = st.session_state.picked
    export = df[df["country"].isin(picked)][["country", "year", "co2", "co2_per_capita", "population", "gdp"]]
    st.download_button("Télécharger les données (CSV)", export.to_csv(index=False).encode("utf-8"),
                       file_name="co2_pays_selectionnes.csv", mime="text/csv", icon=":material/download:",
                       disabled=export.empty)
    st.caption("Source : Our World in Data")

cur = df[df["year"] == year]
co2 = cur.dropna(subset=["co2"])
pc = cur.dropna(subset=["co2_per_capita"])
page = st.session_state.page

SUBS = {
    "Vue d’ensemble": "Le tableau de bord en un coup d’œil : le volume des émissions des pays, les principaux émetteurs et l’évolution des émissions dans le temps.",
    "Classement": "Qui émet le plus ? Le classement change selon que l’on compte le total d’un pays ou ce que représente chaque habitant.",
    "Évolution": "Comparez la trajectoire de plusieurs pays dans le temps pour voir qui réduit ses émissions et qui les augmente.",
    "Carte du monde": "Repérez en un regard les régions les plus émettrices, en total ou par habitant.",
    "PIB et CO₂": "Les pays riches émettent-ils plus ? Chaque bulle est un pays : plus elle est grande, plus il est peuplé.",
    "Guide et méthode": "D’où viennent les données, comment lire les indicateurs et quelles sont les limites de l’analyse.",
}
st.markdown(
    f'<div class="topbar"><span class="pill">Analyse de données · <b>{AUTHOR}</b></span>'
    f'<span class="pill">Année {year}</span></div>'
    f'<div class="page-title">{page}</div><div class="page-sub">{SUBS[page]}</div>',
    unsafe_allow_html=True,
)

if page == "Vue d’ensemble":
    total = co2["co2"].sum()
    st.markdown(
        f'<p class="hero-label">Émissions annuelles de CO₂ des pays en {year}</p>'
        f'<div class="hero-number">{fmt(total)}<span class="hero-unit">millions de tonnes</span></div>',
        unsafe_allow_html=True,
    )
    st.write("")
    if not co2.empty:
        top = co2.loc[co2["co2"].idxmax()]
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi("Plus grand émetteur", top["country"], f"{fmt(top['co2'])} Mt"), unsafe_allow_html=True)
        if not pc.empty:
            tp = pc.loc[pc["co2_per_capita"].idxmax()]
            c2.markdown(kpi("Plus fort par habitant", tp["country"], f"{tp['co2_per_capita']:.1f} t / habitant"), unsafe_allow_html=True)
        c3.markdown(kpi("Pays avec données", str(co2["country"].nunique()), f"année {year}"), unsafe_allow_html=True)
        if total > 0:
           top3 = co2.nlargest(3, "co2")["co2"].sum() / total * 100
        else:
           top3 = 0
        c4.markdown(kpi("Part des 3 premiers", f"{top3:.0f} %", "des émissions des pays"), unsafe_allow_html=True)
    st.write("")

    world = df.groupby("year")["co2"].sum().reset_index()
    fig = px.area(world, x="year", y="co2", labels={"year": "", "co2": "Mt de CO₂"})
    fig.update_traces(line=dict(color=SECONDARY, width=3), fillcolor="rgba(249, 115, 22, 0.15)")
    fig.add_vline(x=year, line_dash="dot", line_color=ACCENT)
    st.markdown("### Somme des émissions des pays depuis 1950")
    st.plotly_chart(style(fig, 380), width="stretch")
    with st.expander("Comment lire ce graphique ?"):
        st.write("La courbe additionne les émissions de tous les pays pour chaque année. "
                 "La ligne pointillée marque l’année choisie dans le menu de gauche. "
                 "Une pente qui s’aplatit signale un ralentissement de la hausse, pas une baisse.")
    base = world[world["year"] == 2000]["co2"]
    if year > 2000 and not base.empty:
        insight(f"Depuis 2000, les émissions annuelles des pays ont varié de <b>{(total / base.iloc[0] - 1) * 100:+.0f} %</b>.")

elif page == "Classement":
    explain("Ce que vous voyez",
            "Les pays classés par émissions. En <b>total</b>, les grands pays dominent. "
            "<b>Par habitant</b>, ce sont souvent de petits pays producteurs d’énergie qui arrivent en tête.")
    k1, k2 = st.columns([1, 1])
    with k1:
        mode = st.segmented_control("Indicateur", ["co2", "co2_per_capita"], default="co2",
                                    format_func=LABELS.get, key="rk_mode") or "co2"
    with k2:
        n = st.segmented_control("Nombre de pays", [5, 10, 15, 20], default=10, key="rk_n") or 10
    data = cur.dropna(subset=[mode])
    if mode == "co2_per_capita":
        data = data[data["population"] > 1_000_000]
    top = data.nlargest(n, mode).sort_values(mode)
    fig = px.bar(top, x=mode, y="country", orientation="h", color=mode, color_continuous_scale=HEAT,
                 labels={mode: LABELS[mode], "country": ""})
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style(fig, 90 + 38 * n), width="stretch")
    if not top.empty:
        lead = top.iloc[-1]
        insight(f"En {year}, <b>{lead['country']}</b> est en tête avec <b>{lead[mode]:,.1f}</b> ({LABELS[mode]}).".replace(",", " "))
    if mode == "co2_per_capita":
        st.caption("Les pays de moins d’un million d’habitants sont exclus pour éviter les cas extrêmes.")
    with st.expander("Comment lire ce graphique ?"):
        st.write("Chaque barre est un pays. Plus elle est longue, plus l’indicateur est élevé. "
                 "Changez d’indicateur avec les boutons pour voir comment le classement se transforme.")

elif page == "Évolution":
    explain("Ce que vous voyez",
            "Une ligne par pays sélectionné. Choisissez les pays dans le menu de gauche ou utilisez les boutons "
            "<b>Maghreb</b>, <b>Géants</b> et <b>Europe</b> pour des comparaisons prêtes à l’emploi.")
    metric = st.segmented_control("Indicateur", list(LABELS), default="co2_per_capita",
                                  format_func=LABELS.get, key="ev_metric") or "co2_per_capita"
    if picked:
        ev = df[df["country"].isin(picked)].dropna(subset=[metric])
        fig = px.line(ev, x="year", y=metric, color="country", color_discrete_sequence=SEQ,
                      labels={"year": "", metric: LABELS[metric], "country": ""})
        fig.update_traces(line=dict(width=3))
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(style(fig, 470), width="stretch")
        chg = ev.sort_values("year").groupby("country")[metric].agg(["first", "last"])
        chg = chg[chg["first"] > 0]
        if not chg.empty:
            chg["var"] = (chg["last"] / chg["first"] - 1) * 100
            b, w = chg["var"].idxmin(), chg["var"].idxmax()
            insight(f"Entre la première et la dernière année disponible, <b>{b}</b> affiche la plus forte baisse "
                    f"(<b>{chg.loc[b, 'var']:+.0f} %</b>) et <b>{w}</b> la plus forte hausse (<b>{chg.loc[w, 'var']:+.0f} %</b>).")
        with st.expander("Comment lire ce graphique ?"):
            st.write("Passez la souris sur une année pour comparer tous les pays à la fois. "
                     "Une courbe qui descend indique un pays qui réduit ses émissions. "
                     "Utilisez « par habitant » pour comparer des pays de tailles très différentes.")
    else:
        st.info("Aucun pays sélectionné. Choisissez-en dans le menu de gauche ou cliquez sur Réinitialiser.")

elif page == "Carte du monde":
    explain("Ce que vous voyez",
            "Chaque pays est coloré selon son niveau d’émissions : du bleu clair (peu) au rouge-orangé (beaucoup). "
            "Changez l’année dans le menu de gauche pour voir la carte évoluer.")
    mm = st.segmented_control("Indicateur", ["co2_per_capita", "co2"], default="co2_per_capita",
                              format_func=LABELS.get, key="map_metric") or "co2_per_capita"
    md = cur.dropna(subset=[mm])
    fig = px.choropleth(md, locations="iso_code", color=mm, hover_name="country",
                        color_continuous_scale=HEAT, labels={mm: LABELS[mm]})
    fig.update_geos(showframe=False, showcoastlines=False, bgcolor="rgba(0,0,0,0)",
                    projection_type="natural earth", landcolor="#F1F5F9", showcountries=False)
    fig.update_layout(coloraxis_colorbar=dict(title="", thickness=12, len=0.6))
    st.plotly_chart(style(fig, 560), width="stretch")
    with st.expander("Comment lire cette carte ?"):
        st.write("En total, la carte met en avant les très grands pays. Par habitant, elle montre plutôt "
                 "l’intensité des émissions de chaque personne, ce qui change complètement les couleurs.")

elif page == "PIB et CO₂":
    explain(
        "Ce que vous voyez",
        "Chaque bulle représente un pays : position horizontale = "
        "<b>PIB par habitant</b> (échelle logarithmique), "
        "position verticale = <b>CO₂ par habitant</b>. "
        "La taille de la bulle représente la population."
    )

    gdp_data = df.dropna(subset=["gdp", "population", "co2_per_capita"]).copy()
    gdp_data = gdp_data[
        (gdp_data["gdp"] > 0) &
        (gdp_data["population"] > 0) &
        (gdp_data["co2_per_capita"] >= 0)
    ].copy()

    if not gdp_data.empty:
        gdp_year = int(gdp_data["year"].max())
        sc = gdp_data[gdp_data["year"] == gdp_year].copy()
        sc["gdp_per_capita"] = sc["gdp"] / sc["population"]
        sc = sc[
            (sc["gdp_per_capita"] > 0) &
            np.isfinite(sc["gdp_per_capita"]) &
            np.isfinite(sc["co2_per_capita"])
        ]

        if len(sc) > 2:
            r = np.corrcoef(np.log10(sc["gdp_per_capita"]), sc["co2_per_capita"])[0, 1]

            fig = px.scatter(
                sc, x="gdp_per_capita", y="co2_per_capita", size="population",
                color="co2_per_capita", hover_name="country", log_x=True,
                color_continuous_scale=HEAT, size_max=46,
                labels={"gdp_per_capita": "PIB par habitant", "co2_per_capita": "CO₂ par habitant (t)"}
            )

            sel = sc[sc["country"].isin(picked)]
            if not sel.empty:
                fig.add_scatter(
                    x=sel["gdp_per_capita"], y=sel["co2_per_capita"],
                    mode="markers+text", text=sel["country"],
                    textposition="top center", marker=dict(size=9, color=TEXT),
                    showlegend=False, hoverinfo="skip"
                )

            fig.update_layout(coloraxis_showscale=False)

            a, b = st.columns(2)
            a.markdown(kpi("Corrélation (PIB en log)", f"{r:.2f}", "entre −1 et +1"), unsafe_allow_html=True)
            b.markdown(kpi("Pays analysés", str(len(sc)), f"année {gdp_year}"), unsafe_allow_html=True)

            st.caption(f"Année utilisée : {gdp_year}. Cette année correspond à la dernière année disponible pour les trois indicateurs.")
            st.plotly_chart(style(fig, 520), width="stretch")

            insight("Une corrélation positive indique une association entre le PIB par habitant et les émissions par habitant. <b>Corrélation ne signifie pas causalité.</b>")

            with st.expander("Qu’est-ce que la corrélation ?"):
                st.write("Un nombre entre −1 et +1. Proche de +1 : association positive. Proche de 0 : absence de relation linéaire marquée. Proche de −1 : association négative.")
        else:
            st.warning("Données insuffisantes pour calculer la corrélation.")
    else:
        st.warning("Aucune donnée PIB exploitable n'est disponible.")

else:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### Les indicateurs")
        st.markdown(
            "- **CO₂ total (Mt)** : quantité totale de CO₂ émise par un pays au cours d'une année, exprimée en millions de tonnes.\n"
            "- **CO₂ par habitant (t)** : émissions annuelles de CO₂ divisées par la population du pays.\n"
            "- **CO₂ cumulé (Mt)** : quantité de CO₂ accumulée au fil du temps.\n"
            "- **PIB par habitant** : produit intérieur brut divisé par la population."
        )
    with c2:
        st.markdown("### Méthode et limites")
        st.markdown(
            "- **Source** : jeu de données public *CO₂ and Greenhouse Gas Emissions* d’Our World in Data.\n"
            "- **Périmètre** : uniquement les pays disposant d’un code ISO à trois lettres, à partir de 1950.\n"
            "- **Données manquantes** : certains indicateurs ne sont pas disponibles pour tous les pays.\n"
            "- **PIB** : l'analyse utilise uniquement les observations disponibles.\n"
            "- **Corrélation** : mesure une association statistique, pas une causalité.\n"
            "- **Limite** : les émissions territoriales ≠ empreinte carbone liée à la consommation."
        )
    insight("Pour une lecture rapide : commencez par <b>Vue d’ensemble</b>, puis comparez les pays dans <b>Évolution</b>.")

st.markdown(f'<p class="foot">Conçu par <b>{AUTHOR}</b> · Données : Our World in Data · Python, pandas, Plotly, Streamlit</p>', unsafe_allow_html=True)