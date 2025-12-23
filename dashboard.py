import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Deficiency Management Dashboard",
    layout="wide"
)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    df = pd.read_excel("deficiency_data.xlsx")
    return df

df = load_data()

# ------------------ HEADER ------------------
st.markdown(
    """
    <h1 style='color:#003366;'>Deficiency Management Dashboard</h1>
    <p style='font-size:16px;'>Executive overview of control deficiencies</p>
    """,
    unsafe_allow_html=True
)

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("🔍 Filters")

year = st.sidebar.multiselect("Year", sorted(df["Year"].dropna().unique()))
identified_by = st.sidebar.multiselect("Identified By", df["Identified By"].dropna().unique())
issue_type = st.sidebar.multiselect("Type", df["Type"].dropna().unique())
business_segment = st.sidebar.multiselect("Business Segment", df["Business Segment"].dropna().unique())
location = st.sidebar.multiselect("Location", df["Location"].dropna().unique())
rating = st.sidebar.multiselect("Rating", df["Rating"].dropna().unique())

# ------------------ APPLY FILTERS ------------------
filtered_df = df.copy()

if year:
    filtered_df = filtered_df[filtered_df["Year"].isin(year)]
if identified_by:
    filtered_df = filtered_df[filtered_df["Identified By"].isin(identified_by)]
if issue_type:
    filtered_df = filtered_df[filtered_df["Type"].isin(issue_type)]
if business_segment:
    filtered_df = filtered_df[filtered_df["Business Segment"].isin(business_segment)]
if location:
    filtered_df = filtered_df[filtered_df["Location"].isin(location)]
if rating:
    filtered_df = filtered_df[filtered_df["Rating"].isin(rating)]

# ------------------ KPI METRICS ------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Issues", len(filtered_df))
col2.metric("ICFR Issues", len(filtered_df[filtered_df["Type"] == "ICFR"]))
col3.metric("Operational Issues", len(filtered_df[filtered_df["Type"] == "Operational"]))
col4.metric(
    "Material Weakness",
    len(filtered_df[filtered_df["Would individual conclude the deficiency is a material weakness"] == "Yes"])
)
col5.metric("Unique Locations", filtered_df["Location"].nunique())

# ------------------ CHARTS ------------------
st.subheader("📊 Issues by Business Segment")

fig1 = px.bar(
    filtered_df,
    x="Business Segment",
    color="Type",
    title="Issues Distribution by Business Segment"
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("📈 Issues Trend by Year")

fig2 = px.line(
    filtered_df.groupby("Year").size().reset_index(name="Count"),
    x="Year",
    y="Count",
    markers=True
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------ DATA TABLE ------------------
st.subheader("📋 Detailed Issue List")
st.dataframe(filtered_df, use_container_width=True)
