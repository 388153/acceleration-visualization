import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Title and Description
st.set_page_config(page_title="Acceleration Data Dashboard", layout="wide")
st.subheader("📊 Acceleration Data Visualization")
#st.markdown("Explore acceleration patterns from the `Cavi.csv` dataset.")

# 2. Load the Data
@st.cache_data
def load_data():
    df = pd.read_csv('Cavi.csv')
    # Rename the first column if it's an index
    if 'Unnamed: 0' in df.columns:
        df = df.rename(columns={'Unnamed: 0': 'Index'})
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
targets = df['Target'].unique().tolist()
selected_targets = st.sidebar.multiselect("Select Target Category", targets, default=targets)

# Filter dataframe based on selection
filtered_df = df[df['Target'].isin(selected_targets)]

# 4. Display Basic Metrics
#st.subheader("Summary Metrics")
#col1, col2, col3 = st.columns(3)
#col1.metric("Total Rows", len(filtered_df))
#col2.metric("Avg Abs Acceleration", f"{filtered_df['Abdsolute acceleration (m/s^2)'].mean():.4f}")
#col3.metric("Max Abs Acceleration", f"{filtered_df['Abdsolute acceleration (m/s^2)'].max():.4f}")

# 5. Interactive Plots
#st.subheader("Data Visualizations")

tab1, tab2, tab3 = st.tabs(["Line Chart", "Box Plot", "Raw Data"])

with tab1:
    st.write("### Acceleration over Time/Index")
    # Choose columns to plot
    columns_to_plot = st.multiselect(
        "Select Axes to View", 
        ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', 'Abdsolute acceleration (m/s^2)'],
        default=['Abdsolute acceleration (m/s^2)']
    )
    
    if columns_to_plot:
        # Using Plotly for interactive zoom
        fig_line = px.line(filtered_df, x='Index', y=columns_to_plot, color='Target',
                          title="Acceleration Trends", labels={'value': 'm/s^2'})
        st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.write("### Distribution by Target")
    feature = st.selectbox("Select Feature for Box Plot", 
                          ['Acceleration x (m/s^2)', 'Acceleration y (m/s^2)', 'Acceleration z (m/s^2)', 'Abdsolute acceleration (m/s^2)'])
    
    fig_box = px.box(filtered_df, x='Target', y=feature, color='Target', points="all",
                    title=f"Distribution of {feature} by Category")
    st.plotly_chart(fig_box, use_container_width=True)

with tab3:
    st.write("### Raw Data Preview")
    st.dataframe(filtered_df, use_container_width=True)

# 6. Simple Streamlit Native Chart
#st.divider()
#st.subheader("Quick Native Line Chart")
#st.line_chart(filtered_df.set_index('Index')[['Abdsolute acceleration (m/s^2)']])