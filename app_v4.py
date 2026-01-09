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
st.write("Select PEG properties to filter products and receive rule-based recommendations.")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("peg_products_v2.csv")
df.columns = df.columns.str.strip()  # clean column names

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
    functional_groups,
    default=functional_groups
)

# Polymer Architecture
architectures = sorted(df["Polymer Architecture"].dropna().unique())
selected_arch = st.sidebar.multiselect(
    "Polymer Architecture",
    architectures,
    default=architectures
)

# Intended Application
applications = sorted(df["Intended Application"].dropna().unique())
selected_app = st.sidebar.multiselect(
    "Intended Application",
    applications,
    default=applications
)

# Solubility
solubilities = sorted(df["Solubility"].dropna().unique())
selected_sol = st.sidebar.multiselect(
    "Solubility",
    solubilities,
    default=solubilities
)

# Commercial Partner - LAST filter
partners = sorted(df["Commercial Partner"].dropna().unique())
selected_partner = st.sidebar.multiselect(
    "Commercial Partner",
    partners,
    default=partners
)

# -----------------------------
# Apply filters
# -----------------------------
filtered_df = df[
    (df["Molecular Weight (kDa)"].between(mw_range[0], mw_range[1])) &
    (df["Functional Group / Reactivity"].isin(selected_fg)) &
    (df["Polymer Architecture"].isin(selected_arch)) &
    (df["Intended Application"].isin(selected_app)) &
    (df["Solubility"].isin(selected_sol)) &
    (df["Commercial Partner"].isin(selected_partner))
]

# -----------------------------
# Recommendation score & explanation
# -----------------------------
def recommendation_score_and_explanation(row):
    score = 0
    reasons = []

    if row["Functional Group / Reactivity"] in selected_fg:
        score += 2
        reasons.append("Matches functional group")
    if row["Polymer Architecture"] in selected_arch:
        score += 1
        reasons.append("Matches polymer architecture")
    if row["Intended Application"] in selected_app:
        score += 2
        reasons.append("Matches intended application")
    if row["Solubility"] in selected_sol:
        score += 1
        reasons.append("Matches solubility")

    explanation = ", ".join(reasons)
    return score, explanation

filtered_df[["Recommendation Score", "Recommendation Explanation"]] = filtered_df.apply(
    lambda row: pd.Series(recommendation_score_and_explanation(row)),
    axis=1
)

# Sort by score descending, then MW ascending
filtered_df = filtered_df.sort_values(
    by=["Recommendation Score", "Molecular Weight (kDa)"],
    ascending=[False, True]
)

# -----------------------------
# Results summary
# -----------------------------
st.subheader(f"Filtered Results ({len(filtered_df)} PEGs)")

# CSV Export
st.download_button(
    label="📤 Download filtered results (CSV)",
    data=filtered_df.drop(columns=["Recommendation Score", "Recommendation Explanation"]).to_csv(index=False),
    file_name="peg_selector_filtered_results.csv",
    mime="text/csv"
)

# -----------------------------
# Display results with top recommendation highlight
# -----------------------------
if not filtered_df.empty:
    top_score = filtered_df["Recommendation Score"].max()

for _, row in filtered_df.iterrows():
    badge = "🏆 Recommended" if row["Recommendation Score"] == top_score else ""
    with st.expander(f"{badge} 🧪 {row['Product Name']}  |  Score: {row['Recommendation Score']}"):
        # Top PEG highlighted visually
        if row["Recommendation Score"] == top_score:
            st.markdown(
                "<div style='background-color:#FFF3CD; padding:8px; border-radius:5px;'>"
                "<strong>🏆 Top Recommended PEG</strong>"
                "</div>",
                unsafe_allow_html=True
            )
        # Short explanation text
        st.markdown(f"**Why this PEG is recommended:** {row['Recommendation Explanation']}")
        st.markdown(f"**Molecular Weight (kDa):** {row['Molecular Weight (kDa)']}")
        st.markdown(f"**Functional Group / Reactivity:** {row['Functional Group / Reactivity']}")
        st.markdown(f"**Polymer Architecture:** {row['Polymer Architecture']}")
        st.markdown(f"**Intended Application:** {row['Intended Application']}")
        st.markdown(f"**Polydispersity Index (PDI):** {row['Polydispersity Index (PDI)']}")
        st.markdown(f"**Solubility:** {row['Solubility']}")
        st.markdown(f"**Commercial Partner:** {row['Commercial Partner']}")
        if pd.notna(row["Vendor Product Page"]):
            st.markdown(
                f"🔗 **Vendor Product Page:** [{row['Vendor Product Page']}]({row['Vendor Product Page']})"
            )
