import streamlit as st
import pandas as pd
import plotly.express as px

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
    st.subheader("4.3. Pooled Model Results and Interpretation")
    # Load model stats
    st.markdown("""

The pooled linear regression model was estimated to understand how different marketing campaigns and social media efforts are associated with changes in total revenue collected by businesses (`Amount_Collected`). This model combines all firm types into a single dataset and evaluates overall trends. Below (see Figure 8), we present the summary output from the pooled linear regression model, estimated on the full dataset. The model includes all campaign and platform variables along with their interaction terms. 
""")

    st.image("Figures/pooled_ols_summary.png", width=600)
    st.caption("**Figure 8:** OLS Regression Results (Pooled Model)")

    st.markdown("""


The model explains about **44.6%** of the variation in total revenue, as indicated by the **R-squared** value of **0.446**. This means that nearly half of the differences we see in revenue across businesses can be linked to variations in their marketing strategies and platform usage. The **Adjusted R-squared**, which accounts for the number of variables included, is slightly lower at **0.433**, suggesting a strong explanatory power even after correcting for model complexity.

The model’s **F-statistic is 33.73**, and the associated probability is virtually zero (**p < 0.0001**), confirming that the overall model is statistically significant — in other words, the marketing variables jointly help explain changes in revenue.

The model-level indicators such as the **Akaike Information Criterion (AIC)** and **Bayesian Information Criterion (BIC)** — recorded as **57,250** and **57,450**, respectively — provide reference points for comparing with alternative model specifications. Lower values of AIC and BIC generally indicate a better model fit when comparing across models.

So, it is safe to conclude that the model is statistically significant and reasonably effective at capturing how marketing inputs relate to business performance. 
""")

    st.markdown("""
    Below in (**Table 1**) are the statistically significant predictors (`p < 0.05`) from the pooled linear regression model. These help identify which marketing channels and combinations most strongly influence revenue. Let's look into our statistically significant predictors—those with a p-value less than 0.05.
    """)

    st.subheader("4.3.1. Statistically Significant Predictors (p < 0.05)")
    
    st.markdown("""
    
    **Table 1** and **Figure 9** demonstrate the result of our regression analysis. For instance, the coefficient for **TikTok** is **17.12**.
    which means, holding other variables constant, a 1-unit increase in TikTok investment is associated with an increase of approximately **\$17.12** in revenue.
    Similarly, for **Facebook**, the model estimates an average return of about **$11.57** for every 1-unit increase in Facebook activity.

    In summary:
    - Investing in **TikTok** yields the highest return per unit spent.
    - **Facebook**, **Instagram**, and **YouTube** also show strong positive effects on revenue.
    - **Campaign_Flyer** stands out among the traditional outreach methods with a $2.08 return per unit.
    - Some combinations (e.g., **Facebook × Instagram**) have marginal or near-zero impact, indicating possible redundancy or diminishing returns from overlapping audiences.

   """)

with col2:

    st.dataframe(
    filtered_summary.style.format({
        "Coefficient (Impact)": "{:,.2f}",
        "P-Value": "{:.4f}"
    }),
    use_container_width=False,
    height=500
)   
    st.caption("**Table 1:** Statistically Significant Predictors (p < 0.05) from the Pooled Linear Regression Model")


# Filter and sort statistically significant predictors
    filtered_plot_data = filtered_summary.copy()
    filtered_plot_data = filtered_plot_data[filtered_plot_data['Coefficient (Impact)'] != 0]
    filtered_plot_data = filtered_plot_data.sort_values('Coefficient (Impact)', ascending=True)

        
        # Plotly chart with Southeastern Green accent
    fig = px.bar(
        filtered_plot_data,
        x="Coefficient (Impact)",
        y="Variable",
        orientation="h",
        # title="Figure 9. Statistically Significant Predictors from the Pooled Linear Model",
        text="Coefficient (Impact)",
        labels={"Variable": "Predictor", "Coefficient (Impact)": "Impact on Revenue ($)"},
        height=600,
        color_discrete_sequence=["#1A5632"]  # Southeastern Green
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))

    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 9:** Statistically Significant Predictors from the Pooled Linear Model")

    # Optional download
    csv_data = filtered_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
    "📥Download Statisticaly Significant Results (CSV)",
    data=csv_data,
    file_name="pooled_model_summary.csv",
    mime="text/csv"
)   
    st.subheader("4.4. Segment-Specific Model Results and Interpretation")

    st.markdown("""
While the pooled model gives us a general understanding of which marketing channels are effective, it assumes that all businesses respond similarly. 
To test this assumption, we ran separate linear regression models for each business type (e.g., Small Facility, Private Facility, Medium Facility, Large Facility).

Each model uses the same structure as the pooled model: it includes individual marketing variables, social media platforms, and interaction terms. 
By running the regression separately for each business category, we can capture segment-specific behaviors that would otherwise be averaged out in the pooled model.

The table and chart below summarize the **statistically significant predictors (p < 0.05)** within each business segment. 
This helps us identify **what works for whom** — which marketing strategies are most effective depending on the business type.

For example:
- Some smaller businesses may benefit more from flyers or Facebook, while larger facilities may see stronger returns from TikTok or cross-platform campaigns.
- The direction and strength of these relationships vary, reinforcing that a one-size-fits-all marketing plan may not be optimal.

Segment-specific results give us a more nuanced view of the effectiveness of marketing strategies across business types, and will serve as a foundation for future targeted recommendations.
""")
    
with col2:

    
    st.markdown("Next, we estimated Segment-Specific Models to understand how marketing strategies differ across business types.")

    st.subheader("4.4.1. Medium Facility")
    st.markdown("""
    Figure 10 demonstrates that, about **45% of the variation in revenue**, as shown by the **R-squared of 0.447**. The **adjusted R-squared**, which adjusts for the number of variables used, is **0.397**. Both suggest a reasonably good fit given the complexity of the model.

The **F-statistic (8.998)** and its extremely small p-value indicate that, overall, the model is statistically significant. In other words, these predictors together do a good job explaining revenue outcomes in this segment.

The model used **414 business-month observations**, and produced **AIC = 15,610** and **BIC = 15,750**, which will be useful for comparing across segments.

""")
    st.image("Figures/Medium_Facility_OLS_Summary.png", width=650)
    st.caption("**Figure 10:** OLS Regression Output for Medium Facility")
    
with col2:
    st.markdown("##### Statistically Significant Predictors (p < 0.05)")
    st.markdown("""
Below is the filtered list of variables that are statistically significant at the 5% level for **Medium Facilities**. These represent the most influential marketing levers for this business segment.

The regression coefficient reflects the expected dollar change in revenue from a one-unit increase in that variable, holding all else constant.

Interaction terms (e.g., `Facebook × YouTube`) show how joint strategies perform compared to their individual effects—positive values suggest synergy, while negative ones may indicate overlap or diminishing returns.
    """)

    # Load data
    df_medium = pd.read_csv("Outputs/Medium_Facility_summary.csv")

    # Format and clean
    df_medium = df_medium.dropna()
    df_medium['Coefficient (Impact)'] = df_medium['Coefficient (Impact)'].astype(float)
    df_medium['P-Value'] = df_medium['P-Value'].astype(float)

    # Show formatted table
    st.dataframe(
        df_medium.style.format({
            "Coefficient (Impact)": "{:,.2f}",
            "P-Value": "{:.4f}"
        }),
        use_container_width=False,
        height=500
    )
    st.caption("**Table 2:** Statistically Significant Predictors (p < 0.05) from the Medium Facility Linear Regression Model")
    # Download button
    csv = df_medium.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Medium Facility Summary (CSV)",
        data=csv,
        file_name='Medium_Facility_summary.csv',
        mime='text/csv'
    )


with col2:
    st.markdown("---")
    st.subheader("4.4.1.1. Statistically Significant Predictors")

    st.markdown("""
This section summarizes the key variables from the Medium Facility model that are statistically significant at the **5% level**. These predictors had a measurable and reliable impact on the amount of revenue collected, helping us understand which marketing strategies worked best for this business segment.

The **regression coefficient** represents the expected change in `Amount_Collected` (in dollars) for a one-unit increase in that variable, holding all others constant. For example, a coefficient of 11.50 on `Facebook` means that each additional dollar of investment in Facebook marketing is associated with an average **$11.50 increase in revenue** for medium-sized businesses.

Large negative coefficients can also emerge—for instance, if a strategy not only fails to help but may actively harm revenue. Such is the case with `Campaign_Phone`, whose coefficient of **-2,479** (clipped in the chart) indicates a strongly adverse effect, possibly due to overuse or client aversion to phone-based campaigns.

Interaction terms (e.g., `Campaign_Phone × Facebook`) reveal how combined marketing efforts behave differently than individual ones. A positive interaction implies synergy, while a negative one suggests overlap, redundancy, or even conflict between strategies.
""")

    # Captioned Table
    st.caption("**Table 6:** Statistically Significant Predictors from the Medium Facility Segment")
    st.dataframe(
        df_medium.style.format({
            "Coefficient (Impact)": "{:,.2f}",
            "P-Value": "{:.4f}"
        }),
        use_container_width=True,
        height=520
    )

    # Download button
    csv_medium = df_medium.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Medium Facility Summary (CSV)",
        data=csv_medium,
        file_name="Medium_Facility_Summary.csv",
        mime="text/csv"
    )

    # Bar chart
    st.image("Figures/Medium_Facility_Coefficient_Barplot_Capped.png", use_column_width=True)
    st.caption("**Figure 11:** Impact of Statistically Significant Predictors on Revenue for Medium Facilities")







####################################################################################### Footer
    st.markdown("---")
    st.markdown(
    """
    <style>
      /* hide default Streamlit footer/menu */
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      /* custom footer styling without band */
      .custom-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: right; 
        font-size: 0.8rem;
        color: black;  /* Set text color to black */
        padding: 8px 16px;
        background: transparent; 
      }
    </style>
    <div class="custom-footer">
      © Business Research Center, Southeastern Louisiana University
    </div>
    """,
    unsafe_allow_html=True,
)