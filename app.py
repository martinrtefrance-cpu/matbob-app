import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import base64
import os
from utils import load_data

# ── Charte graphique RTE ─────────────────────────────────────────────────────
RTE_BLUE  = "#009FE3"
RTE_DARK  = "#003F6B"
RTE_LIGHT = "#E6F5FC"
RTE_GREY  = "#F4F6F8"
RTE_TEXT  = "#1A1A2E"
RTE_WHITE = "#FFFFFF"

PALETTE = [
    "#009FE3","#003F6B","#00C4B4","#F5A623",
    "#7ED321","#BD10E0","#E8453C","#4A90D9",
    "#50C878","#FF6B35",
]

st.set_page_config(
    page_title="RTE – Gestion BDD Matériel",
    page_icon="data/RTE_logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global charte RTE ─────────────────────────────────────────────────────
def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {RTE_TEXT};
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {RTE_DARK} 0%, #005A96 100%) !important;
        border-right: none !important;
    }}
    [data-testid="stSidebar"] * {{ color: {RTE_WHITE} !important; }}
    [data-testid="stSidebar"] .stCaption {{ color: rgba(255,255,255,0.55) !important; }}
    [data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.2) !important; }}
    [data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        color: {RTE_WHITE} !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(255,255,255,0.15) !important;
        border-color: rgba(255,255,255,0.5) !important;
    }}
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: {RTE_BLUE} !important;
        border-color: {RTE_BLUE} !important;
        font-weight: 700 !important;
    }}
    .rte-header {{
        background: linear-gradient(135deg, {RTE_DARK} 0%, {RTE_BLUE} 100%);
        padding: 1.4rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.4rem;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        box-shadow: 0 4px 15px rgba(0,159,227,0.25);
    }}
    .rte-header h1 {{
        color: white !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        margin: 0 !important; padding: 0 !important;
    }}
    .rte-header p {{
        color: rgba(255,255,255,0.82) !important;
        margin: 0.2rem 0 0 0 !important;
        font-size: 0.88rem !important;
    }}
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border-left: 4px solid {RTE_BLUE};
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        height: 100%;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,159,227,0.18);
    }}
    .kpi-label {{
        font-size: 0.76rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.06em;
        color: #6B7280; margin-bottom: 0.3rem;
    }}
    .kpi-value {{
        font-size: 1.9rem; font-weight: 700;
        color: {RTE_DARK}; line-height: 1.1;
    }}
    .kpi-sub {{ font-size: 0.76rem; color: #9CA3AF; margin-top: 0.15rem; }}
    .section-title {{
        font-size: 1rem; font-weight: 600; color: {RTE_DARK};
        padding-bottom: 0.35rem;
        border-bottom: 2px solid {RTE_BLUE};
        margin-bottom: 0.7rem;
    }}
    .stButton > button[kind="primary"] {{
        background: {RTE_BLUE} !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,159,227,0.35) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button[kind="primary"]:hover {{
        background: {RTE_DARK} !important;
        box-shadow: 0 4px 14px rgba(0,63,107,0.4) !important;
    }}
    .stDownloadButton > button {{
        background: white !important; color: {RTE_BLUE} !important;
        border: 2px solid {RTE_BLUE} !important;
        border-radius: 8px !important; font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }}
    .stDownloadButton > button:hover {{
        background: {RTE_BLUE} !important; color: white !important;
    }}
    [data-testid="stExpander"] {{
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important; overflow: hidden;
    }}
    [data-testid="stExpander"] summary {{
        background: {RTE_GREY} !important;
        font-weight: 600 !important; color: {RTE_DARK} !important;
    }}
    [data-testid="stMetric"] {{
        background: white; border-radius: 10px;
        padding: 0.8rem 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 3px solid {RTE_BLUE};
    }}
    [data-testid="stMetricLabel"] {{ color: #6B7280 !important; font-size:0.82rem !important; }}
    [data-testid="stMetricValue"] {{ color: {RTE_DARK} !important; font-weight:700 !important; }}
    [data-testid="stDataFrame"] {{
        border-radius: 10px; overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    .stApp {{ background-color: {RTE_GREY}; }}
    .block-container {{ padding-top: 1.4rem !important; padding-bottom: 2rem !important; }}
    </style>
    """, unsafe_allow_html=True)

inject_css()

# ── Logo base64 ───────────────────────────────────────────────────────────────
def get_logo_b64():
    p = "data/RTE_logo.png"
    if os.path.exists(p):
        with open(p, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

LOGO_B64 = get_logo_b64()

def page_header(title, subtitle=""):
    logo_html = f'<img src="data:image/png;base64,{LOGO_B64}" style="height:52px;border-radius:8px;"/>' if LOGO_B64 else ""
    st.markdown(f"""
    <div class="rte-header">
        {logo_html}
        <div>
            <h1>{title}</h1>
            {"<p>" + subtitle + "</p>" if subtitle else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(label, value, sub="", accent=RTE_BLUE):
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color:{accent}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {"<div class='kpi-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """, unsafe_allow_html=True)

def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if LOGO_B64:
        st.markdown(
            f'<div style="text-align:center;padding:1rem 0 0.5rem;">'
            f'<img src="data:image/png;base64,{LOGO_B64}" style="width:78px;border-radius:50%;"/>'
            f'</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-size:0.95rem;font-weight:700;'
        'letter-spacing:0.08em;padding-bottom:0.2rem;">BDD MATÉRIEL</div>',
        unsafe_allow_html=True)
    st.markdown('<hr style="margin:0.5rem 0 1rem;"/>', unsafe_allow_html=True)

    PAGES = {
        "📊  Dashboard":        "dashboard",
        "🗄️  Base de données":  "bdd",
        "✏️  Demandes":         "demandes",
        "🔐  Administration":   "admin",
    }
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    for label, key in PAGES.items():
        if st.button(label, use_container_width=True,
                     type="primary" if st.session_state.page == key else "secondary",
                     key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown('<hr style="margin:1rem 0 0.5rem;"/>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.7rem;color:rgba(255,255,255,0.5);text-align:center;">'
        "Réseau de Transport d'Électricité<br/>Gestion des équipements réseau</div>",
        unsafe_allow_html=True)

# ── Chart defaults ────────────────────────────────────────────────────────────
CHART = dict(
    plot_bgcolor="white", paper_bgcolor="white",
    font=dict(family="Inter, sans-serif", color=RTE_TEXT),
    margin=dict(t=28, b=8, l=8, r=8),
)

@st.cache_data(ttl=30)
def get_data():
    return load_data()


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "dashboard":
    df = get_data()
    page_header("Tableau de bord", "Vue d'ensemble des demandes d'équipements réseau")

    assigned = df["Affectation PLQF"].notna().sum()
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Total demandes", len(df), accent=RTE_BLUE)
    with k2: kpi_card("Sites CRPT", df["CRPT"].nunique(), accent=RTE_DARK)
    with k3: kpi_card("Types de BIS", df["Type de BIS"].nunique(), accent="#00C4B4")
    with k4: kpi_card("Affectées PLQF", assigned,
                       sub=f"{int(100*assigned/len(df))} % du total", accent="#F5A623")

    st.markdown("<br/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        section_title("Demandes par site (CRPT)")
        c = df["CRPT"].value_counts().reset_index(); c.columns = ["CRPT","Nombre"]
        fig = px.bar(c, x="Nombre", y="CRPT", orientation="h",
                     color="CRPT", color_discrete_sequence=PALETTE, text="Nombre")
        fig.update_layout(showlegend=False, height=310, **CHART,
                          yaxis_title="", xaxis_title="Nombre de demandes")
        fig.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_title("Répartition par programme industriel")
        p = df["Programme industrielle"].value_counts().reset_index(); p.columns = ["Programme","Nombre"]
        fig2 = px.pie(p, names="Programme", values="Nombre",
                      color_discrete_sequence=PALETTE, hole=0.45)
        fig2.update_layout(height=310, **CHART)
        fig2.update_traces(textinfo="percent+label", textfont_size=12,
                           marker=dict(line=dict(color="white", width=2)))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        section_title("Demandes par type de BIS")
        b = df["Type de BIS"].value_counts().reset_index(); b.columns = ["Type BIS","Nombre"]
        fig3 = px.bar(b, x="Type BIS", y="Nombre",
                      color="Type BIS", color_discrete_sequence=PALETTE, text="Nombre")
        fig3.update_layout(showlegend=False, height=310, **CHART,
                           xaxis_title="", yaxis_title="Nombre", xaxis_tickangle=-30)
        fig3.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        section_title("Répartition par sous-politique")
        s = df["Sous-politique"].value_counts().reset_index(); s.columns = ["Sous-politique","Nombre"]
        fig4 = px.bar(s, x="Sous-politique", y="Nombre",
                      color="Sous-politique", color_discrete_sequence=PALETTE, text="Nombre")
        fig4.update_layout(showlegend=False, height=310, **CHART,
                           xaxis_title="", yaxis_title="Nombre", xaxis_tickangle=-30)
        fig4.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    col5, col6 = st.columns([2, 1])
    with col5:
        section_title("Évolution des mises en service (MES PFM1)")
        df_mes = df.dropna(subset=["MES PFM1"]).copy()
        df_mes["Année-Mois"] = df_mes["MES PFM1"].dt.to_period("M").astype(str)
        ts = df_mes.groupby("Année-Mois").size().reset_index(name="Nombre").sort_values("Année-Mois")
        fig5 = px.area(ts, x="Année-Mois", y="Nombre", color_discrete_sequence=[RTE_BLUE])
        fig5.update_traces(line=dict(width=2.5), fillcolor="rgba(0,159,227,0.13)")
        fig5.update_layout(height=310, **CHART, xaxis_title="", yaxis_title="Mises en service",
                           xaxis_tickangle=-45)
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        section_title("Huile / Air")
        dh = df.copy(); dh["Huile/Air"] = dh["Huile/Air"].str.lower().str.strip()
        ha = dh["Huile/Air"].value_counts().reset_index(); ha.columns = ["Type","Nombre"]
        fig6 = px.pie(ha, names="Type", values="Nombre",
                      color_discrete_sequence=[RTE_BLUE, RTE_DARK], hole=0.52)
        fig6.update_layout(height=310, **CHART)
        fig6.update_traces(textinfo="percent+label",
                           marker=dict(line=dict(color="white", width=2)))
        st.plotly_chart(fig6, use_container_width=True)

    section_title("Affectation PLQF – répartition par fournisseur")
    plqf = df["Affectation PLQF"].fillna("Non affecté").value_counts().reset_index()
    plqf.columns = ["Fournisseur","Nombre"]
    fig7 = px.bar(plqf, x="Fournisseur", y="Nombre",
                  color="Fournisseur", color_discrete_sequence=PALETTE, text="Nombre")
    fig7.update_layout(showlegend=False, height=330, **CHART,
                       xaxis_title="", yaxis_title="Nombre de demandes", xaxis_tickangle=-30)
    fig7.update_traces(textposition="outside", marker_line_width=0)
    st.plotly_chart(fig7, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# BASE DE DONNÉES
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "bdd":
    import io
    df = get_data()
    page_header("Base de données", f"{len(df)} entrées · Filtrage, recherche et export")

    with st.expander("🔍 Filtres avancés", expanded=True):
        f1, f2, f3 = st.columns(3)
        with f1:
            crpt_opts = ["Tous"] + sorted(df["CRPT"].dropna().unique().tolist())
            sel_crpt = st.selectbox("Site (CRPT)", crpt_opts)
        with f2:
            prog_opts = ["Tous"] + sorted(df["Programme industrielle"].dropna().unique().tolist())
            sel_prog = st.selectbox("Programme industriel", prog_opts)
        with f3:
            bis_opts = ["Tous"] + sorted(df["Type de BIS"].dropna().unique().tolist())
            sel_bis = st.selectbox("Type de BIS", bis_opts)

        f4, f5, f6 = st.columns(3)
        with f4:
            sp_opts = ["Tous"] + sorted(df["Sous-politique"].dropna().unique().tolist())
            sel_sp = st.selectbox("Sous-politique", sp_opts)
        with f5:
            ha_opts = ["Tous"] + sorted(df["Huile/Air"].dropna().str.lower().unique().tolist())
            sel_ha = st.selectbox("Huile/Air", ha_opts)
        with f6:
            plqf_opts = ["Tous"] + sorted(df["Affectation PLQF"].dropna().unique().tolist())
            sel_plqf = st.selectbox("Affectation PLQF", plqf_opts)

        search = st.text_input("🔎 Recherche libre (nom de projet, poste, RUO…)")

        date_range = None
        mes_min = df["MES PFM1"].dropna().min()
        mes_max = df["MES PFM1"].dropna().max()
        if pd.notna(mes_min) and pd.notna(mes_max):
            date_range = st.date_input(
                "Plage de dates MES PFM1",
                value=(mes_min.date(), mes_max.date()),
                min_value=mes_min.date(), max_value=mes_max.date()
            )

    mask = pd.Series([True] * len(df), index=df.index)
    if sel_crpt != "Tous":   mask &= df["CRPT"] == sel_crpt
    if sel_prog != "Tous":   mask &= df["Programme industrielle"] == sel_prog
    if sel_bis  != "Tous":   mask &= df["Type de BIS"] == sel_bis
    if sel_sp   != "Tous":   mask &= df["Sous-politique"] == sel_sp
    if sel_ha   != "Tous":   mask &= df["Huile/Air"].str.lower() == sel_ha
    if sel_plqf != "Tous":   mask &= df["Affectation PLQF"] == sel_plqf
    if search:
        mask &= df.apply(lambda r: search.lower() in " ".join(r.astype(str)).lower(), axis=1)
    if date_range and len(date_range) == 2:
        d0, d1 = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
        mask &= df["MES PFM1"].isna() | ((df["MES PFM1"] >= d0) & (df["MES PFM1"] <= d1))

    df_filtered = df[mask].drop(columns=["__id__"])
    st.markdown(
        f'<div style="background:{RTE_LIGHT};border-left:4px solid {RTE_BLUE};'
        f'border-radius:6px;padding:0.55rem 1rem;margin-bottom:0.8rem;font-weight:600;">'
        f'🔎 {len(df_filtered)} ligne(s) correspondante(s)</div>',
        unsafe_allow_html=True)

    st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True, height=480)

    st.markdown("---")
    section_title("📥 Exporter les données filtrées")
    ex1, ex2 = st.columns(2)
    with ex1:
        csv = df_filtered.to_csv(index=False, sep=";", encoding="utf-8-sig")
        st.download_button("⬇️ Télécharger en CSV", data=csv,
                           file_name="export_bdd.csv", mime="text/csv",
                           use_container_width=True)
    with ex2:
        buf = io.BytesIO()
        df_filtered.to_excel(buf, index=False)
        st.download_button("⬇️ Télécharger en Excel", data=buf.getvalue(),
                           file_name="export_bdd.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# DEMANDES
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "demandes":
    from utils import load_requests, add_request
    df = get_data()

    page_header("Demande de modification / suppression",
                "Soumettez une demande · Elle sera validée par un administrateur")

    type_dem = st.radio("Type de demande", ["✏️ Modification", "🗑️ Suppression"], horizontal=True)
    type_dem_clean = "Modification" if "Modification" in type_dem else "Suppression"

    df["__label__"] = df.apply(
        lambda r: f"[{r['__id__']}]  {r['CRPT']}  –  {r['Poste']}  –  {r['Nom de projet']}", axis=1)
    label_to_id = dict(zip(df["__label__"], df["__id__"]))

    sel_label = st.selectbox("Sélectionner la ligne concernée", df["__label__"].tolist())
    sel_id = label_to_id[sel_label]
    sel_row = df[df["__id__"] == sel_id].drop(columns=["__id__","__label__"]).T
    sel_row.columns = ["Valeur actuelle"]

    with st.expander("👁️ Voir le détail de la ligne sélectionnée"):
        st.dataframe(sel_row, use_container_width=True)

    st.markdown("---")

    if type_dem_clean == "Modification":
        st.markdown(
            f'<div style="background:{RTE_LIGHT};border-left:4px solid {RTE_BLUE};'
            f'border-radius:6px;padding:0.65rem 1rem;margin-bottom:0.8rem;">'
            f'<strong>Format attendu</strong> — une modification par ligne :<br/>'
            f'<code>Colonne: nouvelle valeur</code></div>', unsafe_allow_html=True)
        desc = st.text_area("Modifications demandées",
                            placeholder="Exemple :\nCRPT: Lyon\nAffectation PLQF: Siemens\nType de BIS: 63-30",
                            height=155)
    else:
        st.markdown(
            f'<div style="background:#FEF3C7;border-left:4px solid #F5A623;'
            f'border-radius:6px;padding:0.65rem 1rem;margin-bottom:0.8rem;">'
            f'⚠️ La suppression sera soumise à validation avant d\'être appliquée.</div>',
            unsafe_allow_html=True)
        desc = st.text_area("Raison de la suppression",
                            placeholder="Expliquez pourquoi cette ligne doit être supprimée…",
                            height=110)

    if st.button("📨 Soumettre la demande", type="primary"):
        if not desc.strip():
            st.error("Veuillez renseigner une description avant de soumettre.")
        else:
            details = " | ".join(
                f"{k}: {v}" for k, v in
                df[df["__id__"] == sel_id].drop(columns=["__id__","__label__"]).iloc[0].items()
                if pd.notna(v))
            add_request(type_dem_clean, sel_id, details[:500], desc.strip())
            st.success("✅ Demande soumise avec succès ! En attente de validation admin.")

    st.markdown("---")
    section_title("📋 Historique de toutes les demandes")
    req_df = load_requests()
    if req_df.empty:
        st.info("Aucune demande enregistrée pour le moment.")
    else:
        st.dataframe(req_df, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# ADMINISTRATION
# ════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "admin":
    from utils import load_requests, save_requests, load_data, save_data, apply_modification

    ADMIN_PASSWORD = "admin1234"
    page_header("Administration", "Validation des demandes de modification et suppression")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.markdown("<br/>", unsafe_allow_html=True)
        _, c, _ = st.columns([1, 1.3, 1])
        with c:
            st.markdown(
                f'<div style="background:white;border-radius:14px;padding:2rem 2rem 1.5rem;'
                f'box-shadow:0 4px 20px rgba(0,0,0,0.1);border-top:4px solid {RTE_BLUE};">'
                f'<div style="text-align:center;margin-bottom:1.2rem;">'
                f'<span style="font-size:2.5rem;">🔐</span><br/>'
                f'<strong style="font-size:1.1rem;color:{RTE_DARK};">Espace Administrateur</strong>'
                f'</div>', unsafe_allow_html=True)
            pwd = st.text_input("Mot de passe", type="password",
                                label_visibility="collapsed",
                                placeholder="Entrez le mot de passe admin…")
            if st.button("Se connecter", type="primary", use_container_width=True):
                if pwd == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect.")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        col_info, col_logout = st.columns([4, 1])
        with col_info:
            st.success("✅ Connecté en tant qu'administrateur")
        with col_logout:
            if st.button("🚪 Se déconnecter", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.markdown("---")
        req_df = load_requests()
        pending = req_df[req_df["statut"] == "En attente"] if not req_df.empty else pd.DataFrame()

        b1, b2, b3 = st.columns(3)
        with b1: kpi_card("Total demandes", len(req_df) if not req_df.empty else 0, accent=RTE_BLUE)
        with b2: kpi_card("En attente", len(pending), accent="#F5A623")
        with b3:
            accepted = len(req_df[req_df["statut"] == "Acceptée"]) if not req_df.empty else 0
            kpi_card("Acceptées", accepted, accent="#7ED321")

        st.markdown("<br/>", unsafe_allow_html=True)
        section_title("📋 Demandes en attente de validation")

        if pending.empty:
            st.info("✅ Aucune demande en attente. Tout est à jour.")
        else:
            for _, row in pending.iterrows():
                icon = "✏️" if row["type"] == "Modification" else "🗑️"
                with st.expander(
                    f"{icon} [#{row['id_demande']}] {row['type']} – Ligne {row['id_ligne']} – {row['date_demande']}"
                ):
                    i1, i2 = st.columns(2)
                    with i1:
                        st.markdown(f"**Type :** `{row['type']}`")
                        st.markdown(f"**Ligne :** `{row['id_ligne']}`")
                        st.markdown(f"**Date :** {row['date_demande']}")
                    with i2:
                        st.markdown(f"**Statut :** `{row['statut']}`")

                    st.markdown("**Détails de la ligne :**")
                    st.code(row["details_ligne"], language=None)
                    st.markdown("**Description :**")
                    st.info(row["description"])

                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button(f"✅ Accepter #{row['id_demande']}",
                                     key=f"acc_{row['id_demande']}", type="primary",
                                     use_container_width=True):
                            db = load_data()
                            id_ligne = int(row["id_ligne"])
                            db = db[db["__id__"] != id_ligne] if row["type"] == "Suppression" \
                                else apply_modification(id_ligne, row["description"], db)
                            save_data(db)
                            req_df.loc[req_df["id_demande"] == row["id_demande"], "statut"] = "Acceptée"
                            save_requests(req_df)
                            get_data.clear()
                            st.success(f"Demande #{row['id_demande']} acceptée et appliquée.")
                            st.rerun()
                    with c2:
                        if st.button(f"❌ Refuser #{row['id_demande']}",
                                     key=f"ref_{row['id_demande']}",
                                     use_container_width=True):
                            req_df.loc[req_df["id_demande"] == row["id_demande"], "statut"] = "Refusée"
                            save_requests(req_df)
                            st.warning(f"Demande #{row['id_demande']} refusée.")
                            st.rerun()

        st.markdown("---")
        section_title("📂 Historique complet")
        if req_df.empty:
            st.info("Aucune demande enregistrée.")
        else:
            sf = st.selectbox("Filtrer par statut", ["Tous","En attente","Acceptée","Refusée"])
            display_df = req_df if sf == "Tous" else req_df[req_df["statut"] == sf]
            st.dataframe(display_df, use_container_width=True)
