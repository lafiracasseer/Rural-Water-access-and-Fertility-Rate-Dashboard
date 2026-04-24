
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Water Access & Fertility Rates",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
# Background
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background-color: #000000;
    background-image:
        linear-gradient(rgba(0,0,0,0.90), rgba(0,0,0,0.9)),
        url("https://storagecdn.strathcona.ca/files/filer_public_thumbnails/images/ut-med-rural_water-660x396.jpg__660x396_q85_crop_subsampling-2_upscale.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000000 0%, #1a1a1a 50%, #2b2b2b 100%) !important;
    border-right: 1px solid rgba(100,200,240,0.15);
}
section[data-testid="stSidebar"] * { color: #c8e6f5 !important; }

.hero {
    background: rgba(40,40,40,0.6);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 2rem; font-weight: 700;
    color: #ffffff; margin-bottom: 0.3rem;
}
.hero-sub {
    font-size: 1rem; color: #7ec8e3;
    font-weight: 300; font-style: italic;
}

.kpi-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(100,200,240,0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
    height: 100%;
}
.kpi-val  { font-size: 1.8rem; color: #7ec8e3; font-weight: 600; display: block; }
.kpi-del  { font-size: 0.72rem; color: #4fc97a; display: block; margin: 2px 0; }
.kpi-lab  { font-size: 0.7rem; color: #93b8cc; text-transform: uppercase;
            letter-spacing: 0.08em; display: block; }

.insight {
    background: rgba(61,184,232,0.08);
    border-left: 3px solid #3db8e8;
    border-radius: 0 8px 8px 0;
    padding: 0.8rem 1.1rem;
    margin: 0.8rem 0 1.2rem 0;
    color: #d1d5db ; font-size: 0.9rem; line-height: 1.6;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,27,42,0.6);
    border-radius: 10px; padding: 4px; gap: 4px;
    backdrop-filter: blur(6px);
}
.stTabs [data-baseweb="tab"] {
    color: #9ca3af !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-size: 0.87rem !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(61,184,232,0.18) !important;
    color: #ffffff !important;
}

[data-testid="metric-container"] {
    background: rgba(30,30,30,0.7);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    border: 1px solid rgba(255,255,255,0.08);
}


.section-hdr {
    font-size: 1.1rem; font-weight: 600; color: #7ec8e3;
    border-bottom: 2px solid rgba(100,200,240,0.2); padding-bottom: 0.35rem;
    margin: 1.4rem 0 0.8rem;
}

.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background: rgba(0,0,0,0.8); color: #666;
    text-align: center; padding: 7px;
    font-size: 11px; z-index: 1000;
}
div[data-testid="stRadio"] label {
    color: #ffffff !important;
    font-weight: 500;
}
div[data-testid="stSlider"] label {
    color: #ffffff !important;
    font-weight: 500;
}
div[data-testid="stSlider"] span {
    color: #ffffff !important;  
}
div[data-testid="stRadio"] div {
    color:#ffffff !important;
}
div[data-baseweb="slider"] * {
    color: #ffffff !important;
}
.js-plotly-plot .updatemenu-button {
    color: #ffffff !important;
} 
.js-plotly-plot .xtick text {
    fill: #ffffff !important;
}
div[data-testid="stSelectbox"] label {
    color: #ffffff !important;
    font-weight: 500;
}
div[data-testid="stMetricValue"] {
    color: red !important;
}

[data-testid="stMetric"] [data-testid="stMetricLabel"] * {
    color: #ffffff !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: red !important;
}
.stDownloadButton button {
    color: #000000 !important;
}

#MainMenu, footer, .stDeployButton { visibility: hidden; }
</style>

""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
REGION_COLORS = {
    "Sub-Saharan Africa":         "#e6673d",
    "South Asia":                 "#e8b41a",
    "East Asia & Pacific":        "#35c3c3",
    "Latin America & Caribbean":  "#54d054",
    "Middle East & North Africa": "#b562ed",
    "Europe & Central Asia":      "#29a8db",
}

CHART_LAYOUT = dict(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    font=dict(color="#1a1a1a", family="Inter"),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="rgba(0,0,0,0.1)",
        borderwidth=1, font=dict(size=11,color="#1a1a1a")
    )
)

def style(fig, h=420):
    fig.update_layout(**CHART_LAYOUT, height=h)
    fig.update_xaxes(gridcolor="rgba(0,0,0,0.1)",
                     linecolor="rgba(0,0,0,0.3)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.1)",
                     linecolor="rgba(0,0,0,0.3)", zeroline=False)
    return fig

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(BASE_DIR, "merged_dataset.csv")
        df = pd.read_csv(path)
        df["year"] = df["year"].astype(int)
        df["fertility_rate"] = pd.to_numeric(df["fertility_rate"], errors="coerce")
        df["rural_water_access_pct"] = pd.to_numeric(df["rural_water_access_pct"], errors="coerce")
        df = df.dropna(subset=["fertility_rate", "rural_water_access_pct"])
        df["water_tier"] = pd.cut(
            df["rural_water_access_pct"],
            bins=[0, 40, 70, 90, 100],
            labels=["Very Low (<40%)", "Low (40–70%)", "High (70–90%)", "Universal (>90%)"],
        )
        return df
    except Exception as e:
        st.error(f"Could not load data: {e}")
        return pd.DataFrame()

df_full = load_data()
REGIONS   = sorted(df_full["region"].unique()) if not df_full.empty else []
COUNTRIES = sorted(df_full["country"].unique()) if not df_full.empty else []

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💧Dashboard")
    st.markdown("**Water Access & Fertility Rates**")
    st.markdown("---")
    st.markdown("###  Filters")

    yr_min = int(df_full["year"].min()) if not df_full.empty else 2000
    yr_max = int(df_full["year"].max()) if not df_full.empty else 2021
    year_range = st.slider("Year Range", yr_min, yr_max, (yr_min, yr_max), step=1)

    sel_regions = st.multiselect("Regions", REGIONS, default=REGIONS)

    sel_countries = st.multiselect(
        "Highlight Countries (Trends tab)",
        COUNTRIES,
        default=["India", "Nigeria", "Brazil", "Ethiopia", "Bangladesh"]
    )

    st.markdown("---")
    st.markdown("###  Data Sources")
    st.markdown("""
- **Fertility Rate**  
  World Bank `SP.DYN.TFRT.IN`
- **Rural Water Access**  
  FAO AQUASTAT `FAO_AS_4115`
- **Coverage:** 85 countries  
  6 regions · 2000–2021
    """)

    st.markdown("---")
    # Student details box
    st.markdown("""
    <div style="background:#1a1a1a; border-radius:10px;
                padding:0.9rem 1rem;
                border:1px solid rgba(255,255,255,0.08); font-size:0.88rem;
                line-height:2.0; color:#e5e5e5;">
        <div style="font-weight:700; color:#ffffff; margin-bottom:0.5rem; font-size:0.95rem;">
             Student Details
        </div>
        <b>Name</b><br>Lafira Casseer<br><br>
        <b>UoW Student ID</b><br>W2149495<br><br>
        <b>IIT Student ID</b><br>20232643<br><br>
        <b>Module</b><br>5DATA004C — Data Science Project Lifecycle<br><br>
        <b>Module Leader</b><br>Mr. Fouzul Hassan<br><br>
        <b>University</b><br>University of Westminster
    </div>
    """, unsafe_allow_html=True)

# ── Filter data ────────────────────────────────────────────────────────────────
regions = sel_regions if sel_regions else REGIONS
df = df_full[
    df_full["year"].between(year_range[0], year_range[1]) &
    df_full["region"].isin(regions)
].copy()

# ── Hero Header ────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'> Water Access & Fertility Rates Dashboard</div>
    <div class='hero-sub'>
        How does giving rural communities safe drinking water impact in fertility rates?
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
if not df.empty:
    latest   = df[df["year"] == df["year"].max()]
    earliest = df[df["year"] == df["year"].min()]
    corr_val = df["rural_water_access_pct"].corr(df["fertility_rate"])
    af_now   = latest["fertility_rate"].mean()
    af_then  = earliest["fertility_rate"].mean()
    aw_now   = latest["rural_water_access_pct"].mean()
    aw_then  = earliest["rural_water_access_pct"].mean()

    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, v, lab, d=None):
        d_html = f"<span class='kpi-del'>{d}</span>" if d else ""
        col.markdown(f"""
        <div class='kpi-card'>
            <span class='kpi-val'>{v}</span>{d_html}
            <span class='kpi-lab'>{lab}</span>
        </div>""", unsafe_allow_html=True)

    kpi(k1, f"{af_now:.2f}", "Avg Fertility Rate",
        f"{'↓' if af_now < af_then else '↑'}{abs(af_now - af_then):.2f} since {year_range[0]}")
    kpi(k2, f"{aw_now:.1f}%", "Avg Rural Water Access",
        f"+{aw_now - aw_then:.1f}% since {year_range[0]}")
    kpi(k3, f"{corr_val:.3f}", "Pearson r (Water vs Fertility)")
    kpi(k4, str(df["country"].nunique()), "Countries",
        f"Across {df['region'].nunique()} regions")
    kpi(k5, f"{year_range[1] - year_range[0] + 1} yrs", "Time Span",
        f"{year_range[0]}–{year_range[1]}")

    st.markdown("<br>", unsafe_allow_html=True)


    d = "negative" if corr_val < -0.3 else ("positive" if corr_val > 0.3 else "weak")
    msgs = {
        "negative": f"A correlation of <b>r = {corr_val:.3f}</b> indicates that as rural water access improves, fertility rates tend to <b>decrease</b> — consistent with the demographic transition theory.",
        "positive": f"A correlation of <b>r = {corr_val:.3f}</b> shows a positive association in this filtered view.",
        "weak":     f"A correlation of <b>r = {corr_val:.3f}</b> — weak relationship for this filter. Try expanding the year range or regions.",
    }
    st.markdown(
        f"<div class='insight'> <b>Key Finding :</b>  {msgs[d]}</div>",
        unsafe_allow_html=True
    )

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview",
    "Correlation",
    "World Map",
    "Trends",
    "Analysis",
    "Summary"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    if df.empty:
        st.warning("No data for selected filters.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            rc = df.groupby("region")["country"].nunique().reset_index()
            rc.columns = ["Region", "Countries"]
            fig = px.pie(rc, names="Region", values="Countries",
                         hole=0.38, color="Region",
                         color_discrete_map=REGION_COLORS,
                         title="Countries Analysed by Region")
            fig.update_layout(title={"text": "Countries Analysed by Region","font": {"color": "black", "size": 16} })
            fig.update_traces(textposition="inside", textinfo="percent+label",
                              textfont_size=11 )
            st.plotly_chart(style(fig, 380), use_container_width=True)

        with c2:
            ra = df.groupby("region").agg(
                fertility=("fertility_rate", "mean"),
                water=("rural_water_access_pct", "mean")
            ).reset_index()
            fig2 = px.scatter(ra, x="water", y="fertility",
                              color="region", color_discrete_map=REGION_COLORS,
                              text="region",
                              labels={"water": "Avg Water Access (%)", "fertility": "Avg Fertility Rate"},
                              title="Regional Averages — Water vs Fertility")
            fig2.update_layout(title={"text": "Regional Averages — Water vs Fertility","font": {"color": "black", "size": 16} })
            fig2.update_traces(textposition="top center",
                               marker=dict(size=18, opacity=0.85))
            st.plotly_chart(style(fig2, 380), use_container_width=True)

        st.markdown("---")

        rt = df.groupby(["region", "year"]).agg(
            water=("rural_water_access_pct", "mean"),
            fertility=("fertility_rate", "mean")
        ).reset_index()

        col_a, col_b = st.columns(2)
        with col_a:
            fig3 = px.line(rt, x="year", y="water", color="region",
                           color_discrete_map=REGION_COLORS, markers=True,
                           labels={"year": "Year", "water": "Avg Rural Water Access (%)"},
                           title="Rural Water Access by Region Over Time")
            fig3.update_layout(title={"text": "Rural Water Access by Region Over Time","font": {"color": "black", "size": 16} })
            fig3.update_traces(line_width=2.3, marker_size=4)
            st.plotly_chart(style(fig3, 380), use_container_width=True)

        with col_b:
            fig4 = px.line(rt, x="year", y="fertility", color="region",
                           color_discrete_map=REGION_COLORS, markers=True,
                           labels={"year": "Year", "fertility": "Avg Fertility Rate"},
                           title="Fertility Rate by Region Over Time")
            fig4.update_layout(title={"text": "Fertility Rate by Region Over Time","font": {"color": "black", "size": 16} })
            fig4.update_traces(line_width=2.3, marker_size=4)
            st.plotly_chart(style(fig4, 380), use_container_width=True)

        st.markdown("---")
        st.markdown('<div class="section-hdr"> Regional Comparison (Latest Year)</div>',
                    unsafe_allow_html=True)
        latest_yr  = df["year"].max()
        region_lat = df[df["year"] == latest_yr].groupby("region").agg(
            fertility=("fertility_rate", "mean"),
            water=("rural_water_access_pct", "mean")
        ).reset_index().sort_values("water")

        col_c, col_d = st.columns(2)
        with col_c:
            figb1 = px.bar(region_lat, x="water", y="region", orientation="h",
                           color="region", color_discrete_map=REGION_COLORS,
                           text=region_lat["water"].apply(lambda x: f"{x:.1f}%"),
                           labels={"water": "Rural Water Access (%)", "region": ""},
                           title=f"Rural Water Access by Region ({latest_yr})")
            figb1.update_layout(title={"text": f"Rural Water Access by Region({latest_yr})","font": {"color": "black", "size": 16} })
            figb1.update_traces(textposition="outside")
            figb1.update_layout(showlegend=False)
            st.plotly_chart(style(figb1, 340), use_container_width=True)

        with col_d:
            region_lat2 = region_lat.sort_values("fertility")
            figb2 = px.bar(region_lat2, x="fertility", y="region", orientation="h",
                           color="region", color_discrete_map=REGION_COLORS,
                           text=region_lat2["fertility"].apply(lambda x: f"{x:.2f}"),
                           labels={"fertility": "Avg Fertility Rate", "region": ""},
                           title=f"Fertility Rate by Region ({latest_yr})")
            figb2.update_layout(title={"text": f"Fertility Rate by Region ({latest_yr})","font": {"color": "black", "size": 16} })
            figb2.update_traces(textposition="outside")
            figb2.update_layout(showlegend=False)
            st.plotly_chart(style(figb2, 340), use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CORRELATION EXPLORER  
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    if df.empty:
        st.warning("No data for selected filters.")
    else:
        st.markdown('<div class="section-hdr">Scatter Plot: Water Access vs Fertility Rate</div>',
                    unsafe_allow_html=True)

        col_plot, col_opts = st.columns([3, 1])
        with col_opts:
            colour_by      = st.radio("Colour by", ["Region", "Water Tier", "Year"])
            show_trendline = st.checkbox("OLS trendline", value=True)
            show_labels    = st.checkbox("Country labels", value=True)
            snap_yr        = st.select_slider(
                "Snapshot year",
                options=sorted(df["year"].unique()),
                value=sorted(df["year"].unique())[-1]
            )

        snap_df = df[df["year"] == snap_yr].copy()
        colour_col = {"Region": "region", "Water Tier": "water_tier", "Year": "year"}[colour_by]
        col_map    = REGION_COLORS if colour_by == "Region" else None

        fig_sc = px.scatter(
            snap_df,
            x="rural_water_access_pct",
            y="fertility_rate",
            color=colour_col,
            color_discrete_map=col_map,
            hover_name="country",
            hover_data={"year": True,
                        "rural_water_access_pct": ":.1f",
                        "fertility_rate": ":.2f"},
            trendline="ols" if show_trendline else None,
            opacity=0.65,
            labels={
                "rural_water_access_pct": "Rural Population with Safe Drinking Water (%)",
                "fertility_rate":         "Fertility Rate (births per woman)",
            },
            title=f"Water Access vs Fertility Rate — {snap_yr}",
            height=500,
        )
        fig_sc.update_layout(title={"text": f"Water Access vs Fertility Rate — {snap_yr}","font": {"color": "black", "size": 16} })
        fig_sc.update_traces(marker=dict(size=9, line=dict(width=0.5, color="rgba(255,255,255,0.2)")),
                             selector=dict(mode="markers"))

        if show_labels and sel_countries:
            lbl_df = (
                snap_df[snap_df["country"].isin(sel_countries)]
                .groupby("country")[["rural_water_access_pct", "fertility_rate"]]
                .mean().reset_index()
            )
            for _, row in lbl_df.iterrows():
                fig_sc.add_annotation(
                    x=row["rural_water_access_pct"], y=row["fertility_rate"],
                    text=row["country"], showarrow=True, arrowhead=2,
                    font=dict(size=10, color="#c8e6f5"), arrowcolor="#7ec8e3",
                    arrowwidth=1, ax=25, ay=-22,
                )

        with col_plot:
            st.plotly_chart(style(fig_sc, 500), use_container_width=True)

        # Pearson r over time chart
        st.markdown("---")
        yearly = (
            df.groupby("year")
            .apply(lambda g: g["rural_water_access_pct"].corr(g["fertility_rate"]))
            .reset_index(name="r")
        )
        fig_yr = go.Figure()
        fig_yr.add_trace(go.Scatter(
            x=yearly["year"], y=yearly["r"],
            mode="lines+markers",
            line=dict(color="#3db8e8", width=2.5),
            marker=dict(size=7, color="#7ec8e3"),
            fill="tozeroy", fillcolor="rgba(61,184,232,0.07)",
            hovertemplate="Year: %{x}<br>r = %{y:.3f}<extra></extra>"
        ))
        fig_yr.add_hline(y=0, line_dash="dash", line_color="rgba(200,200,200,0.3)")
        fig_yr.update_layout(title="Pearson Correlation Over Time",
                             xaxis_title="Year", yaxis_title="Pearson r",
                             yaxis=dict(range=[-1, 0.3]))
        fig_yr.update_layout(title={"text": "Pearson Correlation Over Time","font": {"color": "black", "size": 16} })
        st.plotly_chart(style(fig_yr, 300), use_container_width=True)
        
        # Pearson correlation by region table
        st.markdown('<div class="section-hdr">Pearson Correlation by Region</div>',
                    unsafe_allow_html=True)
        rows_r = []
        for reg in sorted(df["region"].unique()):
            sub = df[df["region"] == reg].dropna(subset=["rural_water_access_pct", "fertility_rate"])
            if len(sub) > 5:
                r_r, p_r = stats.pearsonr(sub["rural_water_access_pct"], sub["fertility_rate"])
                rows_r.append({"Region": reg, "Pearson r": round(r_r, 3),
                               "p-value": round(p_r, 4), "n (obs)": len(sub)})
        corr_df = pd.DataFrame(rows_r).sort_values("Pearson r")
        st.dataframe(
            corr_df.style.background_gradient(subset=["Pearson r"], cmap="RdYlGn", vmin=-1, vmax=0),
            use_container_width=True, hide_index=True,
        )

        r_overall = df["rural_water_access_pct"].corr(df["fertility_rate"])
        st.markdown(f"""
        <div class='insight'>
        For the selected filters, the overall Pearson r = <b>{r_overall:.3f}</b>.
        Values closer to <b>-1</b> indicate a stronger negative relationship —
        meaning higher water access is associated with lower fertility rates.
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — WORLD MAP  
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    if df.empty:
        st.warning("No data for selected filters.")
    else:
        map_metric = st.radio(
            "Show on map",
            ["Rural Water Access (%)", "Fertility Rate (births/woman)"],
            horizontal=True
        )
        map_col = ("rural_water_access_pct"
                   if map_metric == "Rural Water Access (%)"
                   else "fertility_rate")

        map_yr_opts = sorted(df["year"].unique())
        map_yr = st.select_slider("Map year", options=map_yr_opts,
                                  value=map_yr_opts[-1], key="map_yr_main")

        map_df_single = df[df["year"] == map_yr].groupby("country")[map_col].mean().reset_index()
        map_df_single.columns = ["country", "value"]

        color_scale = "Blues" if map_col == "rural_water_access_pct" else "OrRd"
        fig_map = px.choropleth(
            map_df_single,
            locations="country", locationmode="country names",
            color="value",
            color_continuous_scale=color_scale,
            hover_name="country",
            hover_data={"value": ":.2f"},
            labels={"value": map_metric},
            title=f"{map_metric} by Country — {map_yr}"
        )
        
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c8e6f5", family="Inter"),
            height=520,
            margin=dict(l=0, r=0, t=50, b=0),
            geo=dict(
                bgcolor="rgba(10,25,47,0.8)",
                landcolor="rgba(40,80,120,0.6)",
                oceancolor="rgba(10,20,40,0.9)",
                showocean=True, showland=True,
                lakecolor="rgba(10,20,40,0.9)",
                framecolor="rgba(100,180,220,0.2)",
            ),
            coloraxis_colorbar=dict(
                tickfont=dict(color="#c8e6f5"),
                title=dict(font=dict(color="#c8e6f5"))
            )
        )
        fig_map.update_layout(title={"text": f"{map_metric} by Country — {map_yr}","font": {"color": "white", "size": 16}})
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown(f"""
        <div class='insight'>
        The map shows <b>{map_metric}</b> for <b>{map_yr}</b>.
        Darker colours on the water map indicate <b>higher water access</b>.
        Darker colours on the fertility map indicate <b>higher fertility rates</b>.
        Notice how the patterns are often <b>inversely related</b>.
        </div>""", unsafe_allow_html=True)

        # Side-by-side comparison maps
        st.markdown('<div class="section-hdr">Side-by-Side Comparison</div>',
                    unsafe_allow_html=True)
        map_df_both = df[df["year"] == map_yr][
            ["country", "rural_water_access_pct", "fertility_rate"]
        ].copy()

        s1, s2 = st.columns(2)
        for col_obj, metric, cscale, title in [
            (s1, "rural_water_access_pct", "Blues", f"Water Access (%) — {map_yr}"),
            (s2, "fertility_rate",         "OrRd",  f"Fertility Rate — {map_yr}"),
        ]:
            fig_s = px.choropleth(
                map_df_both, locations="country", locationmode="country names",
                color=metric, color_continuous_scale=cscale,
                title=title, hover_name="country", height=340,
            )
            fig_s.update_layout(
                margin=dict(t=40, b=0, l=0, r=0),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#c8e6f5"),
                geo=dict(showframe=False, bgcolor="rgba(10,25,47,0.7)",
                         landcolor="rgba(40,80,120,0.5)"),
            )
            fig_s.update_layout(title={"text": f"Water Access (%) — {map_yr}","font": {"color": "white", "size": 16} })
            fig_s.update_layout(title={"text": f"Fertility Rate — {map_yr}","font": {"color": "white", "size": 16} })
            col_obj.plotly_chart(fig_s, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — TRENDS OVER TIME
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    if df.empty:
        st.warning("No data for selected filters.")
    else:
        # Global dual-axis trend 
        st.markdown('<div class="section-hdr">Global Average Trends (2000–2021)</div>',
                    unsafe_allow_html=True)
        trend = (df.groupby("year")[["rural_water_access_pct", "fertility_rate"]]
                 .mean().reset_index())
        fig_tr = make_subplots(specs=[[{"secondary_y": True}]])
        fig_tr.add_trace(
            go.Scatter(x=trend["year"], y=trend["rural_water_access_pct"],
                       name="Rural Water Access (%)",
                       line=dict(color="#3db8e8", width=2.5)),
            secondary_y=False,
        )
        fig_tr.add_trace(
            go.Scatter(x=trend["year"], y=trend["fertility_rate"],
                       name="Fertility Rate",
                       line=dict(color="#e07b5a", width=2.5, dash="dot")),
            secondary_y=True,
        )
        fig_tr.update_layout(title="As Water Access Rises, Fertility Falls",
                             height=420, hovermode="x unified",
                             legend=dict(x=0.01, y=0.99))
        fig_tr.update_layout(title={"text": "As Water Access Rises, Fertility Falls","font": {"color": "black", "size": 16} })
        fig_tr.update_yaxes(title_text="Rural Water Access (%)", secondary_y=False, color="#3db8e8",
                            gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        fig_tr.update_yaxes(title_text="Fertility Rate (births/woman)", secondary_y=True, color="#e07b5a",
                            gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        fig_tr.update_xaxes(gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        fig_tr.update_layout(**{k: v for k, v in CHART_LAYOUT.items() if k != "height"})
        st.plotly_chart(fig_tr, use_container_width=True)

        # Animated scatter 
        st.markdown('<div class="section-hdr">Animated Country Trajectories</div>',
                    unsafe_allow_html=True)
        st.caption("Press ▶ Play to watch how countries shifted from 2000 to 2021")
        anim_df = df[df["year"] % 2 == 0].copy()
        fig_anim = px.scatter(
            anim_df,
            x="rural_water_access_pct", y="fertility_rate",
            animation_frame="year", animation_group="country",
            color="region", hover_name="country",
            color_discrete_map=REGION_COLORS,
            range_x=[0, 105], range_y=[0.5, 9],
            labels={"rural_water_access_pct": "Rural Water Access (%)",
                    "fertility_rate": "Fertility Rate", "region": "Region"},
            title="Country Trajectories 2000–2021 (every 2 years)",
            height=500,
        )
        fig_anim.update_layout(title={"text": "Country Trajectories 2000–2021 (every 2 years)","font": {"color": "black", "size": 16} })
        st.plotly_chart(style(fig_anim, 500), use_container_width=True)

        # Highlighted country dual-panel trends
        if sel_countries:
            st.markdown('<div class="section-hdr">Selected Country Trends</div>',
                        unsafe_allow_html=True)
            cdf = df_full[
                df_full["country"].isin(sel_countries) &
                df_full["year"].between(year_range[0], year_range[1])
            ].sort_values("year")

            if not cdf.empty:
                fig_ct = make_subplots(
                    rows=2, cols=1, shared_xaxes=True,
                    subplot_titles=(
                        "Total Fertility Rate (births per woman)",
                        "Rural Population with Safe Water Access (%)"
                    ),
                    vertical_spacing=0.1
                )
                palette = ["#3db8e8","#e07b5a","#7dd67d","#f5c842","#c084e8","#ff9f7f","#a8dadc"]
                for i, country in enumerate(sel_countries):
                    cd = cdf[cdf["country"] == country]
                    if cd.empty: continue
                    c = palette[i % len(palette)]
                    fig_ct.add_trace(go.Scatter(
                        x=cd["year"], y=cd["fertility_rate"],
                        name=country, line=dict(color=c, width=2.2),
                        mode="lines+markers", marker=dict(size=5),
                        legendgroup=country,
                        hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Fertility: %{{y:.2f}}<extra></extra>"
                    ), row=1, col=1)
                    fig_ct.add_trace(go.Scatter(
                        x=cd["year"], y=cd["rural_water_access_pct"],
                        name=country, line=dict(color=c, width=2.2, dash="dot"),
                        mode="lines+markers", marker=dict(size=5),
                        legendgroup=country, showlegend=False,
                        hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>Water: %{{y:.1f}}%<extra></extra>"
                    ), row=2, col=1)

                fig_ct.update_layout(**CHART_LAYOUT, height=580)
                fig_ct.update_xaxes(title_font=dict(color="white"))
                fig_ct.update_yaxes(title_font=dict(color="white"))
                fig_ct.update_xaxes(gridcolor="rgba(100,180,220,0.08)",
                                    linecolor="rgba(100,180,220,0.15)")
                fig_ct.update_yaxes(gridcolor="rgba(100,180,220,0.08)",
                                    linecolor="rgba(100,180,220,0.15)")
                st.plotly_chart(fig_ct, use_container_width=True)

                # Change summary table
                st.markdown("####  Change Summary")
                rows_t = []
                for country in sel_countries:
                    cd = cdf[cdf["country"] == country].sort_values("year")
                    if len(cd) < 2: continue
                    rows_t.append({
                        "Country": country,
                        "Region": cd["region"].iloc[0],
                        f"Fertility {cd['year'].min()}": f"{cd['fertility_rate'].iloc[0]:.2f}",
                        f"Fertility {cd['year'].max()}": f"{cd['fertility_rate'].iloc[-1]:.2f}",
                        "Δ Fertility": f"{cd['fertility_rate'].iloc[-1] - cd['fertility_rate'].iloc[0]:+.2f}",
                        f"Water {cd['year'].min()}": f"{cd['rural_water_access_pct'].iloc[0]:.1f}%",
                        f"Water {cd['year'].max()}": f"{cd['rural_water_access_pct'].iloc[-1]:.1f}%",
                        "Δ Water": f"+{cd['rural_water_access_pct'].iloc[-1] - cd['rural_water_access_pct'].iloc[0]:.1f}%",
                    })
                if rows_t:
                    st.dataframe(pd.DataFrame(rows_t), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-hdr">Country Analysis</div>', unsafe_allow_html=True)

    default_idx = COUNTRIES.index("India") if "India" in COUNTRIES else 0
    country_sel = st.selectbox("Select a country", COUNTRIES, index=default_idx)
    c_df = df_full[df_full["country"] == country_sel].sort_values("year")

    if c_df.empty:
        st.warning(f"No data for {country_sel}.")
    else:
        # 4 KPI metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Region", c_df["region"].iloc[0])
        m2.metric("Water Access (latest)", f"{c_df['rural_water_access_pct'].iloc[-1]:.1f}%")
        m3.metric("Fertility Rate (latest)", f"{c_df['fertility_rate'].iloc[-1]:.2f}")
        delta_w = c_df["rural_water_access_pct"].iloc[-1] - c_df["rural_water_access_pct"].iloc[0]
        m4.metric("Change in Water Access", f"+{delta_w:.1f} pp")

        # Bar + line chart
        fig_c = make_subplots(specs=[[{"secondary_y": True}]])
        fig_c.add_trace(go.Bar(
            x=c_df["year"], y=c_df["rural_water_access_pct"],
            name="Rural Water Access (%)",
            marker_color="rgba(61,184,232,0.38)",
            marker_line_color="rgba(61,184,232,0.75)",
            marker_line_width=1,
            hovertemplate="Year: %{x}<br>Water: %{y:.1f}%<extra></extra>"
        ), secondary_y=False)
        fig_c.add_trace(go.Scatter(
            x=c_df["year"], y=c_df["fertility_rate"],
            name="Fertility Rate",
            line=dict(color="#e07b5a", width=2.8),
            mode="lines+markers", marker=dict(size=7),
            hovertemplate="Year: %{x}<br>Fertility: %{y:.2f}<extra></extra>"
        ), secondary_y=True)
        fig_c.update_layout(
            **CHART_LAYOUT, height=440,
            title=f"{country_sel} — Fertility Rate vs Rural Water Access",
            barmode="overlay", hovermode="x unified"
        )
        fig_c.update_yaxes(title_text="Rural Water Access (%)", secondary_y=False,
                           gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)",
                           color="#3db8e8")
        fig_c.update_yaxes(title_text="Fertility Rate (births/woman)", secondary_y=True,
                           gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)",
                           color="#e07b5a")
        fig_c.update_xaxes(gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        st.plotly_chart(fig_c, use_container_width=True)

        # Country vs regional average 
        reg_name = c_df["region"].iloc[0]
        reg_avg  = (
            df_full[df_full["region"] == reg_name]
            .groupby("year")[["rural_water_access_pct", "fertility_rate"]]
            .mean().reset_index()
        )
        fig_vs = make_subplots(1, 2, subplot_titles=["Water Access (%)", "Fertility Rate"])
        for metric, col_idx, colour in [
            ("rural_water_access_pct", 1, "#3db8e8"),
            ("fertility_rate",         2, "#e07b5a"),
        ]:
            fig_vs.add_trace(
                go.Scatter(x=c_df["year"], y=c_df[metric],
                           name=country_sel,
                           line=dict(color=colour, width=2),
                           showlegend=(col_idx == 1)),
                row=1, col=col_idx,
            )
            fig_vs.add_trace(
                go.Scatter(x=reg_avg["year"], y=reg_avg[metric],
                           name=f"{reg_name} avg",
                           line=dict(color="#1c5e76", dash="dash", width=1.5),
                           showlegend=(col_idx == 1)),
                row=1, col=col_idx,
            )
        fig_vs.update_layout(
            **CHART_LAYOUT, height=340,
            title=f"{country_sel} vs {reg_name} Regional Average",
            hovermode="x unified"
        )
        fig_vs.update_xaxes(gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        fig_vs.update_yaxes(gridcolor="rgba(100,180,220,0.08)", linecolor="rgba(100,180,220,0.15)")
        st.plotly_chart(fig_vs, use_container_width=True)

        # Bottom KPIs
        country_r = c_df["rural_water_access_pct"].corr(c_df["fertility_rate"])
        fchg = c_df["fertility_rate"].iloc[-1] - c_df["fertility_rate"].iloc[0]

        ck1, ck2, ck3 = st.columns(3)

        def kpi2(col, v, lab, d=None):
            d_html = f"<span class='kpi-del'>{d}</span>" if d else ""
            col.markdown(f"""
            <div class='kpi-card'>
                <span class='kpi-val'>{v}</span>{d_html}
                <span class='kpi-lab'>{lab}</span>
            </div>""", unsafe_allow_html=True)

        kpi2(ck1, f"{country_r:.3f}", "Correlation (r)", "Water vs Fertility")
        kpi2(ck2, f"{fchg:+.2f}", "Fertility Change",
             f"{c_df['year'].min()}–{c_df['year'].max()}")
        kpi2(ck3, f"+{delta_w:.1f}%", "Water Access Change",
             f"{c_df['year'].min()}–{c_df['year'].max()}")
        
        st.markdown("---")
        with st.expander("Raw data table"):
            disp = c_df[["year", "country", "region", "fertility_rate",
                         "rural_water_access_pct", "water_tier"]].reset_index(drop=True)
            disp.columns = ["Year", "Country", "Region", "Fertility Rate",
                            "Water Access (%)", "Water Tier"]
            st.dataframe(disp, use_container_width=True, hide_index=True)

        st.markdown("---")
        st.download_button(
            label=f"⬇ Download {country_sel} Data (CSV)",
            data=c_df.to_csv(index=False).encode(),
            file_name=f"{country_sel}_water_fertility.csv",
            mime="text/csv"
        )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("## Executive Summary")
    st.markdown("---")
    st.markdown("""
    ### Research Question
    > **Does giving rural communities access to safe drinking water increase or decrease fertility rates?**
    """)

    if not df.empty:
        corr_s = df["rural_water_access_pct"].corr(df["fertility_rate"])
        lat_s  = df[df["year"] == df["year"].max()]
        ear_s  = df[df["year"] == df["year"].min()]
        fc_s   = lat_s["fertility_rate"].mean() - ear_s["fertility_rate"].mean()
        wc_s   = lat_s["rural_water_access_pct"].mean() - ear_s["rural_water_access_pct"].mean()
        s1, s2, s3 = st.columns(3)
        s1.metric("Pearson r", f"{corr_s:.3f}", "Water vs Fertility")
        s2.metric("Fertility Change", f"{fc_s:+.2f}", f"Since {year_range[0]}")
        s3.metric("Water Access Change", f"+{wc_s:.1f}%", f"Since {year_range[0]}")

        st.markdown("""
    ### Answer to the Research Question
    The data shows a **strong negative correlation** between rural water access
    and fertility rates across 85 countries from 2000 to 2021.
    Countries that improved rural drinking water access consistently showed
    declining fertility rates over the same period — supporting the hypothesis
    that water access is associated with **lower** fertility rates.

    ### Regional Highlights
    - **Sub-Saharan Africa** — lowest water access (~50%), highest fertility (~5 births/woman)
    - **East Asia & Pacific** — fastest improvement in water access, sharpest fertility decline
    - **South Asia** — steady progress; India and Bangladesh are strong examples
    - **Europe & Central Asia** — near-universal water access, near-replacement fertility

    ### Why This Relationship Exists
    1. **Women's time burden** — without water, women spend hours collecting it, limiting education
    2. **Child survival** — clean water reduces child mortality, reducing the need for larger families
    3. **Education** — water in schools keeps girls enrolled longer, delaying marriage and childbearing
    4. **Development proxy** — water access reflects broader development which consistently lowers fertility

    ### Limitations
    - Correlation does not imply causation — GDP, education, and healthcare also affect fertility
    - Data gaps exist for some countries before 2005
    - The FAO AQUASTAT dataset uses interpolated values for some years
    """)

    st.markdown("---")
    st.markdown("""
    <div class='insight'>
     <b>Data Sources:</b> World Bank SP.DYN.TFRT.IN (Fertility Rate) &
    FAO AQUASTAT FAO_AS_4115 (Rural Water Access) · 85 countries · 2000–2021
    </div>
    """, unsafe_allow_html=True)

