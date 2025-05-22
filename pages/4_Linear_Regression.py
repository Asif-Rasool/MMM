import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Linear Regression",
    layout="wide",
    page_icon="athletic-logo-spirit-mark.svg",
    menu_items={
      'Get Help': None,
      'Report a bug': None,
      'About': None,
          }
)

col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st.markdown("---")
    st.header("4. Linear Regression")
    st.markdown("""
To understand how marketing efforts influence revenue, we estimated two versions of the linear regression model. The first uses the full dataset to capture overall trends across all businesses. The second runs separate models by business type to uncover segment-specific drivers and strategy differences.
""")
    st.subheader("4.1. Pooled Linear Model")
    st.markdown("""
To begin our recommendation system, we estimate a linear regression model where the dependent variable is the total revenue collected (`Amount_Collected`) by a business in a given period. The model aims to explain how marketing investments across various channels contribute to actual sales outcomes.

The estimated model is as follows:

    Amount_Collected = β₀ + β₁(Campaign_Email) + β₂(Campaign_Flyer) + β₃(Campaign_Phone)
                     + β₄(Facebook) + β₅(Instagram) + β₆(YouTube) + β₇(TikTok) + β₈(LinkedIn)
                     + β₉(Campaign_Email × Campaign_Flyer) + ...
                     + βₖ(LinkedIn × TikTok) + ε

In this specification:
- `Campaign_Email`, `Campaign_Flyer`, and `Campaign_Phone` represent direct spending on email, flyer, and phone-based campaigns.
- `Facebook`, `Instagram`, `YouTube`, `TikTok`, and `LinkedIn` represent platform-specific marketing exposure or spending.
- The interaction terms (e.g., `Campaign_Email × Instagram`, `YouTube × TikTok`) capture the joint effect of using two channels simultaneously. These terms help assess whether certain combinations of platforms or campaign types reinforce or dampen each other's impact.
- ε is the error term capturing unobserved factors.

This model includes all pairwise interaction terms between campaign and platform variables. After estimating the model on the full dataset, we identified variables that are statistically significant at the 5% level. These variables are retained in the filtered summary and serve as the key drivers of revenue.
The model's coefficients (β) indicate the expected change in `Amount_Collected` for a one-unit increase in each independent variable, holding all other variables constant. For example, if β₁ = 0.5 for `Campaign_Email`, it suggests that increasing email spending by \$1 is associated with an increase in revenue of $0.50, assuming all other factors remain unchanged.
The model's R-squared value indicates the proportion of variance in `Amount_Collected` explained by the independent variables. A higher R-squared suggests a better fit, but it is essential to consider overfitting, especially with many interaction terms.
""")
    
    st.subheader("4.2. Segment-Specific Linear Models")
    st.markdown("""
While the overall model provides useful insights into average campaign effectiveness, it assumes that all businesses respond similarly to marketing inputs. To test this assumption, we estimated separate linear regression models for each `Client_Type`.

Each model uses the same structure as before, including all campaign variables, platform variables, and their pairwise interaction terms. By isolating the analysis within each business segment, we are able to identify which strategies work best for different types of firms—such as Large, Medium, Private, or Small Facilities.

This segmented approach helps answer one of our core questions: whether marketing strategies need to be tailored based on business type. The results tells us which variables are significant drivers of revenue for each segment, and how the effectiveness of various campaigns and platform combinations may vary across firm types.
""")
    

# Load filtered summary (CSV generated from your notebook)
filtered_summary = pd.read_csv("Outputs/pooled_model_summary.csv")

with col2:
    st.subheader("4.3. Pooled Model Results")
    # Load model stats
    model_stats = pd.read_csv("Outputs/pooled_model_stats.csv")

    # Filter out AIC and BIC
    model_stats = model_stats[~model_stats["Unnamed: 0"].isin(["AIC", "BIC"])]

    model_stats = pd.read_csv("Outputs/pooled_model_stats.csv")
    model_stats = model_stats[~model_stats["Unnamed: 0"].isin(["AIC", "BIC"])]
    model_stats.columns = ["Metric", "Value"]

# Format numbers
    model_stats["Value"] = model_stats["Value"].apply(
    lambda x: f"{x:.4f}" if isinstance(x, float) and abs(x) < 100 else f"{int(x):,}" if x.is_integer() else f"{x:.2f}"
)
    st.table(model_stats.set_index("Metric"))


    st.markdown("""
    This section presents a high-level summary of the pooled linear regression model, including model fit and statistical strength.
    """)

    st.markdown("""
    Below are the statistically significant predictors (`p < 0.05`) from the pooled linear regression model.
    These help identify which marketing channels and combinations most strongly influence revenue.
    """)


    st.dataframe(
        filtered_summary.style.format({
            "Coefficient (Impact)": "{:,.2f}",
            "P-Value": "{:.4f}"
        }),
        use_container_width=False,
        height=500
    )

    # Optional download
    csv_data = filtered_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Significant Results (CSV)",
        data=csv_data,
        file_name="pooled_model_summary.csv",
        mime="text/csv"
    )
