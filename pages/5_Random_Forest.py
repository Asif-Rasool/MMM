import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json

st.set_page_config(
    page_title="Random Forest",
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
    st.header("5. Random Forest")

    st.markdown("""
    To complement our linear regression results and capture non-linearities and higher-order interactions, we train **Random Forest** regression models. A Random Forest is an ensemble of decision trees grown on random bootstrap samples and a random subset of features. Final predictions are the **average** across all trees, reducing over-fitting while modeling complex relationships.

    **Learn more:**  
    [Scikit-learn Random Forest Documentation](https://scikit-learn.org/stable/modules/ensemble.html#forest)
    """)

    # 5.1 Pooled Random Forest
    st.subheader("5.1 Pooled Random Forest")

    st.markdown("""
    We first fit a single Random Forest on the **entire dataset**, using the same eight channel features and all twenty-eight pairwise interaction terms from our OLS specification. The model prediction can be written as:
    """)

    st.latex(r"""
    \hat y \;=\; \frac{1}{T}\sum_{t=1}^{T} \mathrm{Tree}_{t}(\mathbf{x})
    """)

    st.markdown("""
    where:  
    - $\mathbf{x}$ contains our base features  
    (Campaign_Email, Campaign_Flyer, Campaign_Phone, Facebook, Instagram, YouTube, TikTok, LinkedIn)  
    plus every pairwise product (e.g. Campaign_Email × Instagram).  
    - **$T = 200$** is the number of trees in the ensemble.  
    - Each $\mathrm{Tree}_t$ is trained on a bootstrap sample and a random subset of predictors.  

    By averaging across trees, the Random Forest captures complex signal (including non-linear and interaction effects) while stabilizing against over-fitting.
    """)


with col2:
    st.subheader("5.1.1. Pooled Random Forest Results and Interpretation")

    # -- Explanation text
    st.markdown("""
The pooled Random Forest model was estimated on the **full dataset** (200 trees, same eight channels + all pairwise interactions) to predict total revenue collected (`Amount_Collected`).  
""")

    # -- Load metrics from JSON & display as a small table
    metrics = json.load(open("Outputs/rf_metrics.json"))
    st.markdown("""
The pooled Random Forest model—trained on the full dataset with 200 trees and the same eight channels plus all pairwise interactions—achieves strong predictive performance out of sample.  Its Test RMSE is **29,103,805**, indicating the average deviation from actual revenue.  The model explains **36.8 %** of the variance in revenue (Test R² = 0.368) and demonstrates stable generalization across folds (average 5-fold CV R² = 0.417).  
""")


    # -- Load feature importances and show full table

    st.subheader("5.1.2. Top Predictors (Feature Importances)")

    st.markdown("""
    **Table 6** and **Figure 18** summarize the ten most influential features in our pooled Random Forest model.  Importance values reflect each variable’s average contribution to reducing prediction error across all 200 trees.

    - **Campaign Flyer × Instagram (0.296):** The top predictor—combining traditional flyers with Instagram delivers the largest revenue uplift.  
    - **Instagram (0.154):** A strong standalone driver reflecting high engagement.  
    - **Instagram × YouTube (0.133) & YouTube (0.086):** Video platforms and their synergy capture significant gains.  
    - **Facebook × Instagram (0.057) & Facebook × TikTok (0.048):** Cross-platform strategies with Facebook add meaningful lift.  
    - **Campaign Flyer (0.034):** Traditional outreach still matters, though less than digital channels.

    We observed that integrated, multi-channel campaigns—especially those pairing flyers with Instagram—are most effective at driving revenue.
    """)

    fi = pd.read_csv("Outputs/feature_importance.csv")
    fi["Feature"] = (
        fi["feature"]
          .str.replace("_x_", " × ")
          .str.replace("_", " ")
          .str.title()
    )
    fi_display = fi[["Feature","importance"]].rename(columns={"importance":"Importance"})
    
    st.dataframe(
        fi_display.head(10).style.format({"Importance":"{:.3f}"}),
        use_container_width=False, height=300
    )
    st.caption("**Table 6:** Top 10 Feature Importances from the Pooled Random Forest")

    # -- Plotly bar chart
    top10 = fi_display.head(10).sort_values("Importance", ascending=True)
    fig = px.bar(
        top10,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 10 Feature Importances (Pooled RF)",
        labels={"Importance":"Importance","Feature":"Feature"},
        color_discrete_sequence=["#1A5632"]
    )
    fig.update_traces(texttemplate="%{x:.3f}", textposition="outside")
    fig.update_layout(margin=dict(l=150, r=20, t=50, b=50))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 18:** Top 10 Feature Importances from the Pooled Random Forest")

    # -- Download button for importances
    csv_data = fi_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Feature Importances (CSV)",
        data=csv_data,
        file_name="pooled_rf_feature_importance.csv",
        mime="text/csv"
    )

with col2:
    st.subheader("5.1.3. Marginal Effects Interpretation")

    st.markdown("""
For our Random Forest model, the **top five** average marginal revenue uplifts per 1-unit increase are:


These mirror the familiar OLS interpretation (“+1 unit TikTok → $17.12”), but now capture the non-linear and interaction effects learned by the forest.
""" )
    
    
    
    # 1) Load the full marginals JSON
    me = json.load(open("Outputs/rf_marginals_full.json"))
    
    # 2) Build a DataFrame, filter positive, sort, take top 5
    df_me = (
        pd.DataFrame.from_dict(me, orient="index", columns=["Marginal Effect"])
          .query("`Marginal Effect` > 0")
    )
    df_me.index.name = "Feature"
    df_me = df_me.reset_index()
    df_me["Feature"] = (
        df_me["Feature"]
          .str.replace("_x_", " × ")
          .str.replace("_", " ")
          .str.title()
    )
    top5 = df_me.nlargest(5, "Marginal Effect").reset_index(drop=True)
    
    # 3) Display as an interactive, scrollable table
    styled = (
        top5.style
            .format({"Marginal Effect":"${:,.2f}"})
            .set_properties(**{"text-align":"left"})
            .set_table_styles([
                {"selector":"th","props":[("text-align","left")]},
            ])
    )
    st.dataframe(styled, height=200, use_container_width=False)
    
    # 4) Write-up below


    # 5.2 Segment-Specific Random Forests
    st.subheader("5.2 Segment-Specific Random Forests")

    st.markdown("""
    To understand how marketing campaigns vary by business type, next we train separate Random Forests on each segment (Small, Medium, Large Facilities), using the same feature set $\mathbf{x}$. This allows us to compare:
    - Global importance: which channels dominate in each segment?  
    - Marginal effects: how the predicted uplift per-unit of each channel differs across segments.  

    These segment-specific forests will help us to do tailored recommendations for each business category.
    """)














####################################################################################### Footer
with col2:    
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