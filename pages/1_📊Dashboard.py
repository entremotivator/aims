import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

#######################
# Page Configuration
st.set_page_config(
    page_title="n8n AI Agent Management Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

#######################
# CSS Styling
st.markdown("""
<style>
[data-testid="block-container"] {
    padding: 2rem;
    background-color: #f9f9f9;
    border-radius: 10px;
}
[data-testid="stMetric"] {
    background-color: #2E2E2E;
    text-align: center;
    padding: 15px;
    border-radius: 5px;
}
[data-testid="stMetricLabel"] {
    color: #FFFFFF;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

#######################
# Demo Data for Agents with Departments and Shows
@st.cache_data
def load_demo_data():
    np.random.seed(42)
    departments = ["Sales", "Support", "HR", "Tech", "Marketing", "Operations", "Finance", "Customer Success"]
    shows = ["Show A", "Show B", "Show C", "Show D", "Show E", "Show F"]
    agents = [f"Agent {i}" for i in range(1, 51)]  # Increased to 50 agents
    
    data = {
        "Agent": agents,
        "Exactions": np.random.randint(500, 3000, size=50),
        "Failures": np.random.randint(100, 1500, size=50),
        "Region": np.random.choice(["North", "South", "East", "West"], size=50),
        "Department": np.random.choice(departments, size=50),
        "Show": np.random.choice(shows, size=50),
        "Date": [datetime.date(2025, 1, 1) + datetime.timedelta(days=np.random.randint(0, 30)) for _ in range(50)],
    }
    df = pd.DataFrame(data)
    df["Performance (%)"] = round(100 - (df["Failures"] / (df["Exactions"] + df["Failures"])) * 100, 2)
    return df

df_agents = load_demo_data()

#######################
# Sidebar
with st.sidebar:
    st.title("Filters")
    
    selected_date = st.date_input("Filter by Date", value=datetime.date(2025, 1, 10))
    selected_region = st.multiselect("Filter by Region", options=df_agents["Region"].unique(), default=df_agents["Region"].unique())
    selected_department = st.selectbox("Filter by Department", options=["All"] + df_agents["Department"].unique().tolist(), index=0)
    selected_show = st.selectbox("Filter by Show", options=["All"] + df_agents["Show"].unique().tolist(), index=0)
    min_performance = st.slider("Minimum Performance (%)", min_value=0, max_value=100, value=50)

    filtered_data = df_agents[
        (df_agents["Date"] <= selected_date) &
        (df_agents["Region"].isin(selected_region)) &
        (df_agents["Performance (%)"] >= min_performance)
    ]
    
    if selected_department != "All":
        filtered_data = filtered_data[filtered_data["Department"] == selected_department]
    if selected_show != "All":
        filtered_data = filtered_data[filtered_data["Show"] == selected_show]

#######################
# Functions for Visualizations

def plot_exactions_vs_failures(df):
    fig = px.bar(
        df,
        x="Agent",
        y=["Exactions", "Failures"],
        barmode="group",
        title="Exactions vs Failures per Agent",
        labels={"value": "Count", "variable": "Metric"},
        text_auto=True,
    )
    return fig

def plot_pie_chart(df):
    df_summary = df[["Exactions", "Failures"]].sum().reset_index(name="Value")
    fig = px.pie(df_summary, values="Value", names="index", title="Proportion of Exactions to Failures")
    return fig

def plot_performance_trend(df):
    fig = px.line(
        df.sort_values("Date"),
        x="Date",
        y="Performance (%)",
        color="Agent",
        title="Performance Trends Over Time",
        labels={"Performance (%)": "Performance (%)"},
        markers=True,
    )
    return fig

def plot_agent_comparison(df):
    fig = px.scatter(
        df,
        x="Exactions",
        y="Failures",
        size="Performance (%)",
        color="Region",
        hover_name="Agent",
        title="Agent Comparison: Exactions vs Failures",
        labels={"Exactions": "Exactions", "Failures": "Failures"},
    )
    return fig

def plot_radar_chart(df):
    radar_df = df.set_index("Agent")[["Exactions", "Failures", "Performance (%)"]].reset_index()
    radar_df = pd.melt(radar_df, id_vars=["Agent"], var_name="Metric", value_name="Value")
    fig = px.line_polar(radar_df, r="Value", theta="Metric", color="Agent", line_close=True, title="Agent Performance Radar Chart")
    return fig

def predict_future_performance(df):
    df_sorted = df.sort_values("Date")
    X = np.array(range(len(df_sorted))).reshape(-1, 1)
    y = df_sorted["Performance (%)"].values
    model = LinearRegression().fit(X, y)
    future_dates = np.array(range(len(df_sorted), len(df_sorted) + 10)).reshape(-1, 1)
    future_performance = model.predict(future_dates)
    future_df = pd.DataFrame({
        "Date": [df_sorted["Date"].max() + datetime.timedelta(days=i) for i in range(1, 11)],
        "Predicted Performance (%)": future_performance,
    })
    fig = px.line(future_df, x="Date", y="Predicted Performance (%)", title="Future Performance Prediction")
    return fig

def generate_correlation_matrix(df):
    correlation = df[["Exactions", "Failures", "Performance (%)"]].corr()
    fig = px.imshow(correlation, text_auto=True, title="Correlation Matrix")
    return fig

#######################
# Dashboard Main Panel

st.title("AI Agent Management Dashboard")
st.markdown("A comprehensive dashboard for managing and analyzing the performance of your agents.")

# Metrics Section
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Exactions", f"{filtered_data['Exactions'].sum():,}")
with col2:
    st.metric("Total Failures", f"{filtered_data['Failures'].sum():,}")
with col3:
    st.metric("Avg Performance (%)", f"{filtered_data['Performance (%)'].mean():.2f}")
with col4:
    st.metric("Agents Analyzed", f"{len(filtered_data):,}")

# Visualizations
st.markdown("### Visualizations")
st.plotly_chart(plot_exactions_vs_failures(filtered_data), use_container_width=True)
st.plotly_chart(plot_pie_chart(filtered_data), use_container_width=True)
st.plotly_chart(plot_performance_trend(filtered_data), use_container_width=True)
st.plotly_chart(plot_agent_comparison(filtered_data), use_container_width=True)

# Radar Chart
st.markdown("### Agent Radar Comparison")
st.plotly_chart(plot_radar_chart(filtered_data), use_container_width=True)

# Predictive Analysis
st.markdown("### Predictive Performance Analysis")
st.plotly_chart(predict_future_performance(filtered_data), use_container_width=True)

# Correlation Matrix
st.markdown("### Correlation Analysis")
st.plotly_chart(generate_correlation_matrix(filtered_data), use_container_width=True)

# Data Table
st.markdown("### Detailed Agent Data")
st.dataframe(
    filtered_data,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Agent": "Agent Name",
        "Exactions": "Total Exactions",
        "Failures": "Total Failures",
        "Performance (%)": "Performance Percentage",
        "Region": "Assigned Region",
        "Department": "Department",
        "Show": "Show",
    },
)
