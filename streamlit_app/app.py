import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Sales Revenue Dashboard",
    layout="wide"
)

# ---------------- CSS ----------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- TITLE ----------------
st.markdown(
    """
    <h1 style='text-align:center;'>📊 Monthly Revenue Dashboard</h1>
    <p style='text-align:center; color:#9aa0a6;'>
    Business Performance Overview
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload cleaned sales CSV file",
    type=["csv"]
)

# =====================================================
# MAIN LOGIC
# =====================================================
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, sep=";")

    # ---------- VALIDATION ----------
    required_cols = {"year", "month", "revenue"}
    if not required_cols.issubset(df.columns):
        st.error("CSV must contain: year, month, revenue")
        st.stop()

    # ---------- DATE ----------
    df["date"] = pd.to_datetime(
        df["year"].astype(str) + "-" +
        df["month"].astype(str) + "-01"
    )

    df = df.sort_values("date")

    # ---------- SIDEBAR ----------
    st.sidebar.title("⚙️ Dashboard Settings")
    year_selected = st.sidebar.selectbox(
        "Select Year",
        sorted(df["year"].unique())
    )

    df = df[df["year"] == year_selected]

    # ---------- MONTHLY AGGREGATION ----------
    monthly_df = (
    df.groupby("date", as_index=False)["revenue"]
    .sum()
    )

    # ---------- KPI ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-box">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">{df['revenue'].sum():,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-box">
                <div class="kpi-title">Average Monthly Revenue</div>
                <div class="kpi-value">{df['revenue'].mean():,.0f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        best_month = df.loc[df["revenue"].idxmax(), "date"].strftime("%Y-%m")
        st.markdown(
            f"""
            <div class="kpi-box">
                <div class="kpi-title">Best Month</div>
                <div class="kpi-value">{best_month}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- CHART ----------
    fig = px.line(
    monthly_df,
    x="date",
    y="revenue",
    markers=True,
    title="Monthly Revenue Trend",
    template="plotly_dark"
)

    st.plotly_chart(fig, use_container_width=True)

    # ---------- INSIGHT ----------
    st.subheader("🧠 Business Insights")
    st.write(f"""
    • Highest revenue recorded in **{best_month}**  
    • Revenue shows noticeable monthly fluctuation  
    • Dashboard supports business monitoring and reporting  
    """)

# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class="footer">
    Built by Data Analyst Student · Streamlit Dashboard Project
    </div>
    """,
    unsafe_allow_html=True
)
