import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


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
    GITHUB_URL = "https://github.com/Asif-Rasool/MMM"
    COLAB_URL  = "https://colab.research.google.com/github/Asif-Rasool/MMM/blob/main/main.ipynb"

    HEADER_ICONS = f"""
    <div style="float:right; margin:10px 0; display:flex; align-items:center; gap:8px;">
        <a href="{COLAB_URL}" target="_blank">
        <img src="https://colab.research.google.com/assets/colab-badge.svg"
            width="80"
            style="vertical-align:middle;" />
        </a>
        <span style="font-size:18px; line-height:1; color:#666;">|</span>
        <a href="{GITHUB_URL}" target="_blank">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
            width="30"
            style="vertical-align:middle;" />
        </a>
    </div>
    """

    st.markdown(HEADER_ICONS, unsafe_allow_html=True)


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

This model includes all pairwise interaction terms between campaign and platform variables. After estimating the model on the full dataset, we identified variables that are statistically significant at the 5% level. 
The model's coefficients (β) indicate the expected change in `Amount_Collected` for a one-unit increase in each independent variable, holding all other variables constant. For example, if β₁ = 0.5 for `Campaign_Email`, it suggests that increasing email spending by \$1 is associated with an increase in revenue of $0.50, assuming all other factors remain unchanged.
The model's R-squared value indicates the proportion of variance in `Amount_Collected` explained by the independent variables. A higher R-squared suggests a better fit, but it is essential to consider overfitting, especially with many interaction terms.
""")
    
    st.subheader("4.2. Segment-Specific Linear Models")
    st.markdown("""
While our pooled OLS model provides useful insights into average campaign effectiveness, it assumes that all businesses respond similarly to marketing inputs. To test this assumption, we estimated separate linear regression models for each `Client_Type`.

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


The model explains about 44.6% of the variation in total revenue, as indicated by the R-squared value of 0.446. This means that nearly half of the differences we see in revenue across businesses can be linked to variations in their marketing strategies and platform usage. The Adjusted R-squared, which accounts for the number of variables included, is slightly lower at 0.433, suggesting a strong explanatory power even after correcting for model complexity.

The model’s F-statistic is 33.73, and the associated probability is virtually zero (p < 0.0001), confirming that the overall model is statistically significant — in other words, the marketing variables jointly help explain changes in revenue.

The model-level indicators such as the Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC) — recorded as 57,250 and 57,450, respectively — provide reference points for comparing with alternative model specifications. Lower values of AIC and BIC generally indicate a better model fit when comparing across models.

So, it is safe to conclude that the model is statistically significant and reasonably effective at capturing how marketing inputs relate to business performance. 
""")

    st.markdown("""
    Below in (**Table 1**) are the statistically significant predictors (`p < 0.05`) from the pooled linear regression model. These help identify which marketing channels and combinations most strongly influence revenue. Let's look into our statistically significant predictors—those with a p-value less than 0.05.
    """)

    st.subheader("4.3.1. Statistically Significant Predictors (p < 0.05)")
    
    st.markdown("""
    
    **Table 1** and **Figure 9** demonstrate the result of our regression analysis. For instance, the coefficient for TikTok is 17.12.
    which means, holding other variables constant, a 1-unit increase in TikTok investment is associated with an increase of approximately \$17.12 in revenue.
    Similarly, for Facebook, the model estimates an average return of about $11.57 for every 1-unit increase in Facebook activity.

    In summary:
    - Investing in TikTok yields the highest return per unit spent.
    - Facebook, Instagram, and YouTube also show strong positive effects on revenue.
    - Campaign_Flyer stands out among the traditional outreach methods with a $2.08 return per unit.
    - Some combinations (e.g., Facebook × Instagram) have marginal or near-zero impact, indicating possible redundancy or diminishing returns from overlapping audiences.

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
Next, we estimated Segment-Specific Models to understand how marketing strategies differ across business types. While the pooled model gives us a general understanding of which marketing channels are effective, it assumes that all businesses respond similarly. 
To test this assumption, we ran separate linear regression models for each business type (e.g., Small Facility, Private Facility, Medium Facility, Large Facility).

Each model uses the same structure as the pooled model: it includes individual marketing variables, social media platforms, and interaction terms. 
By running the regression separately for each business category, we can capture segment-specific behaviors that would otherwise be averaged out in the pooled model.

For example:
- Some smaller businesses may benefit more from flyers or Facebook, while larger facilities may see stronger returns from TikTok or cross-platform campaigns.
- The direction and strength of these relationships vary, reinforcing that a one-size-fits-all marketing plan may not be optimal.

Segment-specific results give us a more nuanced view of the effectiveness of marketing strategies across business types, and will serve as a foundation for future targeted recommendations.
""")
    
with col2:

    
    st.subheader("4.4.1. Medium Facility")
    st.markdown("""
    Figure 10 demonstrates that, about 45% of the variation in revenue, as shown by the R-squared of 0.447. The adjusted R-squared, which adjusts for the number of variables used, is 0.397. Both suggest a reasonably good fit given the complexity of the model.

The F-statistic (8.998) and its extremely small p-value indicate that, overall, the model is statistically significant. In other words, these predictors together do a good job explaining revenue outcomes in this segment.

The model used 414 business-month observations, and produced AIC = 15,610 and BIC = 15,750, which will be useful for comparing across segments.

""")
    st.image("Figures/Medium_Facility_OLS_Summary.png", width=650)
    st.caption("**Figure 10:** OLS Regression Output for Medium Facility")
    


    # Load data
    df_medium = pd.read_csv("Outputs/Medium_Facility_summary.csv")

    # Format and clean
    df_medium = df_medium.dropna()
    df_medium['Coefficient (Impact)'] = df_medium['Coefficient (Impact)'].astype(float)
    df_medium['P-Value'] = df_medium['P-Value'].astype(float)

 
with col2:
    
    st.subheader("4.4.1.1. Statistically Significant Predictors")

    st.markdown("""

The regression coefficient (please see **Table 2** and **Figure 11**) represents the expected change in `Amount_Collected` (in dollars) for a one-unit increase in that variable, holding all others constant. For example, a coefficient of 11.50 on `Facebook` means that each additional dollar of investment in Facebook marketing is associated with an average $11.50 increase in revenue for medium-sized businesses.

Large negative coefficients can also emerge—for instance, if a strategy not only fails to help but may actively harm revenue. Such is the case with `Campaign_Phone`, whose coefficient of -2,479 (clipped in the chart) indicates a strongly adverse effect, possibly due to overuse or client aversion to phone-based campaigns.

Interaction terms (e.g., `Campaign_Phone × Facebook`) reveal how combined marketing efforts behave differently than individual ones. A positive interaction implies synergy, while a negative one suggests overlap, redundancy, or even conflict between strategies.
""")

    # Captioned Table
    
    st.dataframe(
        df_medium.style.format({
            "Coefficient (Impact)": "{:,.2f}",
            "P-Value": "{:.4f}"
        }),
        use_container_width=True,
        height=520
    )
    st.caption("**Table 2:** Statistically Significant Predictors from the Medium Facility Segment")

    # Download button
    csv_medium = df_medium.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Medium Facility Summary (CSV)",
        data=csv_medium,
        file_name="Medium_Facility_Summary.csv",
        mime="text/csv"
    )

    # Plot: Statistically Significant Predictors for Medium Facility
# Filter and sort statistically significant predictors for Medium Facility
    df_medium_filtered = df_medium[df_medium["Coefficient (Impact)"] != 0]
    df_medium_filtered = df_medium_filtered.sort_values("Coefficient (Impact)", ascending=True)

    import plotly.express as px
    import numpy as np

    # Sort and optionally clip
    plot_data = df_medium_filtered.copy()
    plot_data = plot_data[plot_data["Coefficient (Impact)"] != 0]
    plot_data = plot_data.sort_values("Coefficient (Impact)", ascending=True).reset_index(drop=True)

    # Optional: clip extreme values for visual scaling (but keep original for labels)
    max_display_value = 100  # Adjust this threshold as needed
    plot_data["Display_Coefficient"] = np.clip(plot_data["Coefficient (Impact)"], -max_display_value, max_display_value)
    plot_data["Label"] = plot_data["Coefficient (Impact)"].apply(lambda x: f"{x:.0f}*" if abs(x) > max_display_value else f"{x:.2f}")

    # Plot
    fig = px.bar(
        plot_data,
        x="Display_Coefficient",
        y="Variable",
        orientation="h",
        text="Label",
        labels={"Variable": "Predictor", "Display_Coefficient": "Impact on Revenue ($)"},
        height=700,
        color_discrete_sequence=["#1A5632"]
    )

    fig.update_traces(textposition='outside', textfont_size=11)
    fig.update_layout(
        title="Statistically Significant Predictors for Medium Facility",
        margin=dict(t=60, b=60, l=120, r=60),
        xaxis=dict(range=[plot_data["Display_Coefficient"].min() - 10, plot_data["Display_Coefficient"].max() + 10])
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 11:** Statistically Significant Predictors from the Medium Facility Regression Model  \n*Note: Coefficients marked with `*` have been clipped for visual clarity.")

with col2:
    st.subheader("4.4.2. Large Facility")

    st.markdown("""
**Figure 12** below, summarizes the regression results for Large Facilities. The model explains about 40.2% of the variation in revenue, as indicated by the R-squared of 0.402. After adjusting for the number of predictors, the adjusted R-squared stands at 0.378, suggesting a reasonably good fit for this business segment.

The model’s F-statistic is 16.56, with a p-value effectively equal to zero. This means the overall model is statistically significant—there’s strong evidence that the included marketing variables collectively influence revenue for this segment.

The model used 897 observations from large businesses. The AIC (33,000) and BIC (33,180) values can help benchmark this model's efficiency when compared to other segment-specific models.

""")
    st.image("Figures/Large_Facility_OLS_Summary.png", width=650)
    st.caption("**Figure 12:** OLS Regression Output for Large Facility")


    st.subheader("4.4.2.1. Statistically Significant Predictors")
    st.markdown("""
**Table 3** below, demonstrates predictors that were statistically significant at the 5% level for Large Facilities. The regression coefficient reflects the expected change in revenue for a one-unit increase in that variable, holding all other factors constant. For example, a coefficient of 2.90 means that, on average, a one-unit increase in spending or presence on that platform is associated with a $2.90 increase in revenue.

Notably:
- TikTok (17.12) and Facebook (6.65) had the strongest positive associations with revenue.
- Campaign types like Email and Flyer, as well as Instagram (2.90), also showed consistent positive returns.
- A few interaction terms — such as Campaign_Flyer × Facebook and Instagram × YouTube — were also statistically significant, suggesting joint use of these platforms may have compounded effects.

As before, positive values suggest that increasing activity on that channel or campaign is expected to raise revenue. Interaction terms (e.g., `Campaign_Email × Campaign_Flyer`) indicate whether a combined marketing effort performed differently than the individual effects. 

""")


        # Load data
    df_large_filtered = pd.read_csv("Outputs/Large_Facility_summary.csv")

    # Format and clean
    df_large_filtered = df_large_filtered.dropna()
    df_large_filtered['Coefficient (Impact)'] = df_large_filtered['Coefficient (Impact)'].astype(float)
    df_large_filtered['P-Value'] = df_large_filtered['P-Value'].astype(float)
    # Remove rows where all cells are empty or contain only whitespace
    df_large_filtered = df_large_filtered.reset_index(drop=True)
        
    st.dataframe(
        df_large_filtered.style.format({
            "Coefficient (Impact)": "{:,.2f}",
            "P-Value": "{:.4f}"
        }),
        use_container_width=True,
        height=520
    )
    st.caption("**Table 3:** Statistically Significant Predictors from the Large Facility Segment")

    csv_large = df_large_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Large Facility Summary (CSV)",
        data=csv_large,
        file_name="Large_Facility_Summary.csv",
        mime="text/csv"
    )

    # Plotly Chart
    import plotly.express as px
    fig = px.bar(
        df_large_filtered.sort_values("Coefficient (Impact)", ascending=True),
        x="Coefficient (Impact)",
        y="Variable",
        orientation="h",
        text="Coefficient (Impact)",
        labels={"Variable": "Predictor", "Coefficient (Impact)": "Impact on Revenue ($)"},
        height=600,
        color_discrete_sequence=["#1A5632"]
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(
        title="Statistically Significant Predictors for Large Facility",
        margin=dict(t=50, b=50, l=50, r=50)
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 13:** Statistically Significant Predictors from the")

with col2:
    st.subheader("4.4.3. Small Facility")

    st.markdown("""
**Figure 14** presents the regression results for the Small Facility segment. The model explains only 8.4% of the variation in revenue (R-squared = 0.084), and the adjusted R-squared is slightly negative (-0.007), suggesting that the model does not offer meaningful predictive value for this segment.

The F-statistic (0.9176) and associated p-value (0.546) confirm that the model, as a whole, is not statistically significant. In practical terms, this means that the selected predictors do not explain revenue patterns in this business type as reliably as in others.

Despite the weak overall model fit, we filtered and retained individual variables that were statistically significant (p < 0.05). These predictors are shown in **Table 4** and visualized in **Figure 15**.
""")
    st.image("Figures/Small_Facility_OLS_Summary.png", width=650)
    st.caption("**Figure 14:** OLS Regression Output for Small Facility")

    # Load and clean table
    df_small = pd.read_csv("Outputs/Small_Facility__summary.csv")
    df_small_filtered = df_small[
        (df_small["Variable"] != "Intercept") & (df_small["P-Value"] < 0.05)
    ].copy()
    df_small_filtered = df_small_filtered[
        ~df_small_filtered.apply(lambda row: row.astype(str).str.strip().eq("").all(), axis=1)
    ].reset_index(drop=True)

    # Display table
    st.dataframe(
        df_small_filtered[["Variable", "Coefficient (Impact)", "P-Value", "Client Type"]],
        use_container_width=True
    )
    st.caption("**Table 4:** Statistically Significant Predictors from the Small Facility Segment")

    st.download_button(
        "📥 Download Small Facility Summary (CSV)",
        data=df_small_filtered.to_csv(index=False).encode("utf-8"),
        file_name="Small_Facility_Summary.csv",
        mime="text/csv"
    )

    # Plot chart
    import numpy as np
    import plotly.express as px

    clip_threshold = 100
    df_small_filtered["Display_Coefficient"] = np.clip(df_small_filtered["Coefficient (Impact)"], -clip_threshold, clip_threshold)
    df_small_filtered["Label"] = df_small_filtered["Coefficient (Impact)"].apply(
        lambda x: f"{x:.0f}*" if abs(x) > clip_threshold else f"{x:.2f}"
    )

    fig = px.bar(
        df_small_filtered.sort_values("Coefficient (Impact)"),
        x="Display_Coefficient",
        y="Variable",
        text="Label",
        orientation="h",
        labels={"Variable": "Predictor", "Display_Coefficient": "Impact on Revenue ($)"},
        color_discrete_sequence=["#1A5632"],
        height=700
    )

    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(
        title="Statistically Significant Predictors for Small Facility",
        margin=dict(t=60, b=60, l=120, r=60),
        xaxis=dict(range=[
            df_small_filtered["Display_Coefficient"].min() - 10,
            df_small_filtered["Display_Coefficient"].max() + 10
        ])
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 15:** Statistically Significant Predictors from the Small Facility Regression Model  \n*Note: Coefficients marked with `*` were clipped for readability.")

with col2:
    st.subheader("4.4.4. Private Facility")


    st.markdown("""
**Figure 16** displays the regression results for the Private Facility segment. The model explains about 45.4% of the variation in revenue, based on an R-squared of 0.454. The adjusted R-squared is 0.293, indicating the model still holds predictive value even after accounting for model complexity.

The F-statistic (2.827) and its corresponding p-value (0.00289) indicate that the model is statistically significant overall. Despite the small sample size (only 67 observations), the predictors collectively explain revenue variation reasonably well in this business segment.

""")
    st.image("Figures/Private_Facility_OLS_Summary.png", width=650)
    st.caption("**Figure 16:** OLS Regression Output for Private Facility")
    
    st.subheader("4.4.4.1. Statistically Significant Predictors")
    st.markdown("""
The list of statistically significant predictors is shown in **Table 5**, with their relative magnitudes visualized in **Figure 17**. The coefficient on each variable indicates its expected impact on revenue from a one-unit increase, holding all else constant. For instance, if a coefficient is 2.50, then a one-unit increase in that channel’s activity is associated with a $2.50 increase in monthly revenue.

Notably:
- Several campaign-specific and platform variables had strong positive effects, including combinations like `Campaign_Email × YouTube` and direct platform engagement on Instagram and YouTube.
- While the overall model was statistically significant, the limited sample size (67 observations) means that individual predictors must be interpreted with caution.
- As before, interaction terms (e.g., `Campaign_Flyer × Campaign_Phone`) suggest how joint use of different marketing strategies may amplify or dilute effectiveness compared to running them separately.


""")

    # Load and filter summary table
    df_private = pd.read_csv("Outputs/Private_Facility_summary.csv")
    df_private_filtered = df_private[
        (df_private["Variable"] != "Intercept") & (df_private["P-Value"] < 0.05)
    ].copy()
    df_private_filtered = df_private_filtered[
        ~df_private_filtered.apply(lambda row: row.astype(str).str.strip().eq("").all(), axis=1)
    ].reset_index(drop=True)

    # Display table
    st.dataframe(
        df_private_filtered[["Variable", "Coefficient (Impact)", "P-Value", "Client Type"]],
        use_container_width=True
    )
    st.caption("**Table 5:** Statistically Significant Predictors from the Private Facility Segment")

    st.download_button(
        "📥 Download Private Facility Summary (CSV)",
        data=df_private_filtered.to_csv(index=False).encode("utf-8"),
        file_name="Private_Facility_Summary.csv",
        mime="text/csv"
    )

    # Plotly chart


    clip_threshold = 100
    df_private_filtered["Display_Coefficient"] = np.clip(df_private_filtered["Coefficient (Impact)"], -clip_threshold, clip_threshold)
    df_private_filtered["Label"] = df_private_filtered["Coefficient (Impact)"].apply(
        lambda x: f"{x:.0f}*" if abs(x) > clip_threshold else f"{x:.2f}"
    )

    fig = px.bar(
        df_private_filtered.sort_values("Coefficient (Impact)"),
        x="Display_Coefficient",
        y="Variable",
        text="Label",
        orientation="h",
        labels={"Variable": "Predictor", "Display_Coefficient": "Impact on Revenue ($)"},
        color_discrete_sequence=["#1A5632"],
        height=700
    )

    fig.update_traces(textposition="outside", textfont_size=11)
    fig.update_layout(
        title="Statistically Significant Predictors for Private Facility",
        margin=dict(t=60, b=60, l=120, r=60),
        xaxis=dict(range=[
            df_private_filtered["Display_Coefficient"].min() - 10,
            df_private_filtered["Display_Coefficient"].max() + 10
        ])
    )

    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 17:** Statistically Significant Predictors from the Private Facility Regression Model  \n*Note: Coefficients marked with `*` were clipped for readability.")




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