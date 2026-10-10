# ============================================================
# BankInsight: Customer Intelligence Dashboard

# ============================================================

# ----------------------------
# Imports
# ----------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="BankInsight",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------------------------
# Load Data
# ----------------------------

@st.cache_data
def load_data():

    customers = pd.read_csv("customers_clean.csv")
    transactions = pd.read_csv("transactions_clean.csv")

    return customers, transactions


customers, transactions = load_data()


# ----------------------------
# Create Age Segments
# ----------------------------

age_mapping = {
    29: "Young Professionals",
    30: "Young Professionals",
    44: "Mid-Career Adults",
    45: "Mid-Career Adults",
    59: "Pre-Retirement Adults",
    60: "Pre-Retirement Adults"
}

customers["age_segment"] = customers["age"].map(age_mapping)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏦 BankInsight")

st.sidebar.markdown(
"""
**Customer Intelligence Dashboard**

Use the filters below to explore the data.
"""
)

with st.sidebar.expander("🔎 Dashboard Filters", expanded=True):

    income_filter = st.multiselect(
        "Income Bracket",
        options=sorted(customers["income_bracket"].unique()),
        default=sorted(customers["income_bracket"].unique())
    )

    age_filter = st.multiselect(
        "Age Segment",
        options=sorted(customers["age_segment"].dropna().unique()),
        default=sorted(customers["age_segment"].dropna().unique())
    )

    segment_filter = st.multiselect(
        "Customer Segment",
        options=sorted(customers["customer_segment"].unique()),
        default=sorted(customers["customer_segment"].unique())
    )

    location_filter = st.multiselect(
        "Location",
        options=sorted(customers["location"].unique()),
        default=sorted(customers["location"].unique())
    )

# ----------------------------
# Apply Filters
# ----------------------------


filtered = customers[
    (customers["income_bracket"].isin(income_filter)) &
    (customers["age_segment"].isin(age_filter)) &
    (customers["customer_segment"].isin(segment_filter)) &
    (customers["location"].isin(location_filter))
]


# ============================================================
# DASHBOARD HEADER
# ============================================================

st.title("🏦 BankInsight")

st.markdown(
"""
## Customer Intelligence Dashboard

An executive dashboard designed to monitor customer value,
retention, digital engagement and customer experience.

---
"""
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

filtered_transactions = transactions[
    transactions["customer_id"].isin(filtered["customer_id"])
]

# Customer KPIs
total_customers = len(filtered)

average_products = filtered["active_products"].mean()
average_satisfaction = filtered["satisfaction_score"].mean()
average_nps = filtered["nps_score"].mean()
average_churn = filtered["churn_probability"].mean()
average_clv = filtered["customer_lifetime_value"].mean()

# Transaction KPIs
total_transactions = len(filtered_transactions)
transaction_volume = int(filtered_transactions["amount"].sum())

# ============================================================
# KPI SECTION
# ============================================================

st.subheader("Executive KPIs")


row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)

with row1_col1:

    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with row1_col2:

    st.metric(
        "💳 Transactions",
        f"{total_transactions:,}"
    )

with row1_col3:

    st.metric(
        "💰 Transaction Volume",
        f"{transaction_volume:,.0f}"
    )

with row1_col4:

    st.metric(
        "📦 Avg Products",
        f"{average_products:.2f}"
    )


row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)

with row2_col1:

    st.metric(
        "⭐ Satisfaction",
        f"{average_satisfaction:.2f}"
    )

with row2_col2:

    st.metric(
        "❤️ Average NPS",
        f"{average_nps:.2f}"
    )

with row2_col3:

    st.metric(
        "⚠ Predicted Churn",
        f"{average_churn:.2f}"
    )

with row2_col4:

    st.metric(
        "💵 Average CLV",
        f"{average_clv:,.0f}"
    )

st.markdown("---")
# ============================================================
# CUSTOMER VALUE & RETENTION
# ============================================================

st.markdown(
    """
    <h2 style="
        color:#1E3A8A;
        border-bottom:2px solid #1E3A8A;
        padding-bottom:8px;">
        👥 Customer Value & Retention
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
### Business Question

**Are customers with more banking products associated with lower predicted churn probability?**
""")

# ----------------------------
# Aggregate Data
# ----------------------------

churn_by_products = (
    filtered
    .groupby("active_products", observed=True)
    .agg(
        Average_Churn=("churn_probability", "mean"),
        Customers=("customer_id", "count")
    )
    .reset_index()
)

# ----------------------------
# Plot
# ----------------------------

fig_churn = px.bar(
    churn_by_products,
    x="active_products",
    y="Average_Churn",
    text="Average_Churn",
    color="Average_Churn",
    color_continuous_scale="Blues",
    title="Customers with More Banking Products Exhibit Lower Predicted Churn Risk"
)

fig_churn.update_traces(texttemplate="%{text:.2f}")

fig_churn.update_layout(
    xaxis_title="Number of Active Products",
    yaxis_title="Average Predicted Churn"
)

st.plotly_chart(
    fig_churn,
    use_container_width=True
)

# ----------------------------
# Insight
# ----------------------------

st.success(
"""
### 🔍 Executive Insight

Customers with a greater number of banking products consistently
exhibit lower predicted churn probability.

Customers holding five banking products have approximately
half the predicted churn probability of customers
with only one banking product.
"""
)

# ----------------------------
# Recommendation
# ----------------------------

st.info(
"""
### 📌 Recommended Action

Expand cross-selling initiatives that encourage customers
to adopt additional banking products.

A broader banking relationship is associated with
stronger customer retention.
"""
)

st.markdown("---")


# ============================================================
# DIGITAL ENGAGEMENT
# ============================================================
st.markdown(
    """
    <h2 style="
        color:#0F766E;
        border-bottom:2px solid #0F766E;
        padding-bottom:8px;">
        📱 Digital Engagement
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
### Business Question

**Is greater feature usage diversity associated with higher product satisfaction?**
""")

# ----------------------------
# Aggregate
# ----------------------------

feature_satisfaction = (
    filtered
    .groupby("feature_usage_diversity", observed=True)
    .agg(
        Average_Product_Satisfaction=(
            "product_satisfaction",
            "mean"
        ),
        Customers=(
            "customer_id",
            "count"
        )
    )
    .reset_index()
)

# ----------------------------
# Plot
# ----------------------------

fig_features = px.line(
    feature_satisfaction,
    x="feature_usage_diversity",
    y="Average_Product_Satisfaction",
    markers=True,
    title="Customers Using More Digital Banking Features Report Higher Product Satisfaction"
)

fig_features.update_layout(
    xaxis_title="Feature Usage Diversity",
    yaxis_title="Average Product Satisfaction"
)

st.plotly_chart(
    fig_features,
    use_container_width=True
)

# ----------------------------
# Insight
# ----------------------------

st.success(
"""
### 🔍 Executive Insight

Customers who use a wider variety of digital banking features
consistently report higher product satisfaction.

Feature adoption appears to be an important indicator
of digital engagement.
"""
)

# ----------------------------
# Recommendation
# ----------------------------

st.info(
"""
### 📌 Recommended Action

Encourage customers to explore additional digital banking features
through onboarding campaigns and in-app guidance.

Improving feature adoption may contribute to
higher product satisfaction.
"""
)

st.markdown("---")
# ============================================================
# CUSTOMER EXPERIENCE
# ============================================================

st.markdown(
    """
    <h2 style="
        color:#D97706;
        border-bottom:2px solid #D97706;
        padding-bottom:8px;">
        😊 Customer Experience
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
### Business Question

**Is higher customer satisfaction associated with stronger customer advocacy (Net Promoter Score)?**
""")

# ----------------------------
# Aggregate
# ----------------------------

nps_by_satisfaction = (
    filtered
    .groupby("satisfaction_score", observed=True)
    .agg(
        Average_NPS=("nps_score", "mean"),
        Customers=("customer_id", "count")
    )
    .reset_index()
)

# ----------------------------
# Plot
# ----------------------------

fig_nps = px.line(
    nps_by_satisfaction,
    x="satisfaction_score",
    y="Average_NPS",
    markers=True,
    title="Higher Customer Satisfaction Is Associated with Stronger Customer Advocacy"
)

fig_nps.update_layout(
    xaxis_title="Customer Satisfaction Score",
    yaxis_title="Average Net Promoter Score"
)

st.plotly_chart(
    fig_nps,
    use_container_width=True
)

# ----------------------------
# Insight + Recommendation
# ----------------------------

left, right = st.columns(2)

with left:

    st.success("""
### 🔍 Executive Insight

Customer satisfaction is strongly associated
with Net Promoter Score.

Customers reporting higher satisfaction
are substantially more likely to recommend
the bank's products and services.
""")

with right:

    st.info("""
### 📌 Recommended Action

Continue investing in customer experience
initiatives including product quality,
customer support and service reliability.

Improving customer satisfaction may also
strengthen customer advocacy.
""")

st.markdown("---")
# ============================================================
# TRANSACTION INTELLIGENCE
# ============================================================

st.markdown(
    """
    <h2 style="
        color:#7C3AED;
        border-bottom:2px solid #7C3AED;
        padding-bottom:8px;">
        💳 Transaction Intelligence
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
### Business Question

**What transaction types dominate customer activity?**
""")

transaction_type = (
    filtered_transactions["type"]
    .value_counts()
    .reset_index()
)

transaction_type.columns = [
    "Transaction Type",
    "Transactions"
]

fig_tx = px.bar(
    transaction_type,
    x="Transaction Type",
    y="Transactions",
    color="Transactions",
    title="Distribution of Transaction Types"
)

st.plotly_chart(
    fig_tx,
    use_container_width=True
)

left, right = st.columns(2)

with left:

    st.success("""
### 🔍 Executive Insight

Customer activity is concentrated within
a limited number of transaction types.

Understanding transaction preferences
helps the bank prioritize services
that customers use most frequently.
""")

with right:

    st.info("""
### 📌 Recommended Action

Continue monitoring transaction trends
to identify changing customer behaviour
and opportunities for improving
digital banking services.
""")

st.markdown("---")
# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.markdown(
    """
    <h2 style="
        color:#334155;
        border-bottom:2px solid #334155;
        padding-bottom:8px;">
        📌 Executive Summary
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown("""
### Key Findings

- Customers with more banking products exhibit lower predicted churn probability.

- Greater feature usage is associated with higher product satisfaction.

- Customer satisfaction is strongly associated with stronger Net Promoter Scores.

- Product ownership alone is not associated with Customer Lifetime Value.

- Feature adoption contributes more strongly to product satisfaction than to overall customer satisfaction.
""")

st.markdown("---")

st.caption(
"BankInsight • Customer Intelligence Dashboard • Developed using Python, Streamlit and Plotly"
)