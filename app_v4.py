import streamlit as st
import pandas as pd

# -----------------------------
# App configuration
# -----------------------------
st.set_page_config(
    page_title="PEG Selector — Interactive Prototype",
    layout="wide"
)

st.title("PEG Selector — Interactive Prototype")
st.write("Select PEG properties to filter products.")

# -----------------------------
# Load CSV
# -----------------------------
df = pd.read_csv("peg_products_v2.csv")
df.columns = df.columns.str.strip()  # remove extra spaces

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filter PEG Properties")

# Molecular Weight
mw_min, mw_max = int(df["Molecular Weight (kDa)"].min()), int(df["Molecular Weight (kDa)"].max())
mw_range = st.sidebar.slider(
    "Molecular Weight (kDa)",
    min_value=mw_min,
    max_value=mw_max,
    value=(mw_min, mw_max)
)

# Functional Group
functional_groups = sorted(df["Functional Group / Reactivity"].dropna().unique())
selected_fg = st.sidebar.multiselect(
    "Functional Group / Reactivity",
    functional_groups
)

# Polymer Architecture
architectures = sorted(df["Polymer Architecture"].dropna().unique())
selected_arch = st.sidebar.multiselect(
    "Polymer Architecture",
    architectures
)

# Intended Application
applications = sorted(df["Intended Application"].dropna().unique())
selected_app = st.sidebar.multiselect(
    "Intended Application",
    applications
)

# Solubility
solubilities = sorted(df["Solubility"].dropna().unique())
selected_sol = st.sidebar.multiselect(
    "Solubility",
    solubilities
)

# Commercial Partner - LAST filter
partners = sorted(df["Commercial Partner"].dropna().unique())
selected_partner = st.sidebar.multiselect(
    "Commercial Partner",
    partners
)

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df[
    (df["Molecular Weight (kDa)"].between(mw_range[0], mw_range[1])) &
    ((df["Functional Group / Reactivity"].isin(selected_fg)) if selected_fg else True) &
    ((df["Polymer Architecture"].isin(selected_arch)) if selected_arch else True) &
    ((df["Intended Application"].isin(selected_app)) if selected_app else True) &
    ((df["Solubility"].isin(selected_sol)) if selected_sol else True) &
    ((df["Commercial Partner"].isin(selected_partner)) if selected_partner else True)
]

st.subheader(f"Filtered Results ({len(filtered_df)} PEGs)")

# -----------------------------
# Display results in accordion
# -----------------------------
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        with st.expander(f"{row['Product Name']}"):
            st.markdown(f"**Molecular Weight (kDa):** {row['Molecular Weight (kDa)']}")
            st.markdown(f"**Functional Group / Reactivity:** {row['Functional Group / Reactivity']}")
            st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
            st.markdown(f"**Intended Application:** {row['Intended Application']}")
            st.markdown(f"**Polydispersity Index (PDI):** {row['Polydispersity Index (PDI)']}")
            st.markdown(f"**Solubility:** {row['Solubility']}")
            st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")  # above product page
            st.markdown(f"🔗 [Vendor Product Page]({row['Product Page']})")
