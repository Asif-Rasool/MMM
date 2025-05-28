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

    GITHUB_URL = "https://github.com/Asif-Rasool/MMM"
    GITHUB_ICON = (
        f'<a href="{GITHUB_URL}" target="_blank">'
        f'<img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" '
        f'width="30" style="float:right; margin-top:10px;" />'
        f'</a>'
    )
    st.markdown(GITHUB_ICON, unsafe_allow_html=True)

    st.markdown("---")
    st.header("5. Random Forest")

    st.markdown("""
    To complement our linear regression results and capture non-linearities and higher-order interactions, we train Random Forest regression models. A Random Forest is an ensemble of decision trees grown on random bootstrap samples and a random subset of features. Final predictions are the average across all trees, reducing over-fitting while modeling complex relationships.

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
For our Pooled Forest model, the **top five** average marginal revenue uplifts per 1-unit increase are shown in **Table 7** below. These mirror the familiar OLS interpretation (“+1 unit TikTok → $17.12”), but now capture the non-linear and interaction effects learned by the forest.
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
    st.caption("**Table 7:** The top five average marginal revenue uplifts per 1-unit increase from the Pooled Random Forest")
    
    # 4) Write-up below
    st.markdown("""
    On average, the Random Forest predicts that increasing Instagram activity by one unit yields the largest revenue uplift (≈ \$37,252), followed by TikTok (+\$23,723), Facebook (+\$2,198), and YouTube (+\$211) per unit. Traditional flyer campaigns alone show almost no marginal gain. In plain terms, doubling down on Instagram and TikTok delivers the biggest bang for your marketing buck, while print‐only efforts have very little standalone impact.
    """)

    # 5.2. Segment-Specific Random Forests
    st.subheader("5.2. Segment-Specific Random Forests")

    st.markdown("""
    To explore how marketing drivers differ by facility size, we train separate Random Forest models for each segment (Small, Medium, Private, Large). Each model is fit on its subset of data, using 200 trees and the same feature set as our pooled model—including eight base channels (Campaign_Email, Campaign_Flyer, Campaign_Phone, Facebook, Instagram, YouTube, TikTok, LinkedIn) and all twenty-eight pairwise interactions.

    By comparing out-of-sample performance, feature importances, and marginal effects across segments, we reveal how:

    - Smaller facilities may realize their greatest gains from high-engagement platforms such as Instagram and TikTok.  
    - Larger operations often benefit most when traditional flyers are tightly integrated with social media campaigns.  

    These segment-specific insights allow us to tailor recommendations to each business type rather than rely on a one-size-fits-all strategy.
    """)

    st.subheader("5.2.1.1. Small Facility Random Forest Results and Interpretation")

    # load metrics for this segment
    import json
    mets_sm = json.load(open("Outputs/segments/rf_metrics_Small_Facility.json"))

    st.markdown(f"""
    The Small Facility Random Forest model was trained on the Small Facility subset (200 trees, same eight channels + all pairwise interactions) to predict total revenue collected (`Amount_Collected`). It achieves a Test RMSE of **{mets_sm['rmse']:.0f}**, indicating the average dollar deviation from actual revenue, and explains **{mets_sm['r2']:.1%}** of the variance out of sample. Its average 5-fold CV R² of **{mets_sm['avg_cv_r2']:.3f}** indicates stable generalization across folds.
    """)
    # 5.2.2 Small Facility Top Predictors (Feature Importances)
    st.subheader("5.2.1.2 Small Facility Top Predictors (Feature Importances)")
    st.markdown("""
**Table 8** and **Figure 20** summarize the five most influential features in our **Small Facility** Random Forest model. Importance values reflect each variable’s average contribution to reducing prediction error across all trees.

- **Instagram (0.533):** The single strongest driver—small operations see the greatest revenue boost per unit of Instagram activity.  
- **YouTube (0.215):** A solid secondary channel, reflecting the value of video content.  
- **Campaign Flyer × Instagram (0.142):** Pairing traditional flyers with Instagram amplifies outreach impact.  
- **Instagram × YouTube (0.077):** Cross–video synergies add incremental gains beyond each platform alone.  
- **Campaign Flyer (0.031):** Even at small scale, flyers still deliver a modest lift.
""")

    # Load and prepare the feature‐importance table
    fi_sm = pd.read_csv("Outputs/segments/feature_importance_Small_Facility.csv")
    fi_sm["Feature"] = (
        fi_sm["feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    fi_sm_display = (
        fi_sm[["Feature","importance"]]
        .rename(columns={"importance":"Importance"})
    )

    # Display as dataframe
    st.dataframe(
        fi_sm_display.head(5).style.format({"Importance":"{:.3f}"}),
        use_container_width=False,
        height=250
    )
    st.caption("**Table 8:** Top 5 Feature Importances from the Small Facility Random Forest")

    # Plotly horizontal bar chart
    fig = px.bar(
        fi_sm_display.head(5)[::-1],
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        labels={"Importance":"Importance","Feature":"Feature"},
        title="Small Facility – Top 5 Feature Importances",
        color_discrete_sequence=["#1A5632"]
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(
        margin=dict(l=150, r=20, t=50, b=20),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("**Figure 19:** Top 5 Feature Importances from the Small Facility Random Forest")

    # load the saved marginal effects
    marg_sm = json.load(open("Outputs/segments/rf_marginals_Small_Facility.json"))

    # build a DataFrame
    dfm_sm = (
        pd.DataFrame.from_dict(marg_sm, orient="index", columns=["Marginal Effect"])
        .reset_index()
        .rename(columns={"index":"Feature"})
    )

    # clean up feature names
    dfm_sm["Feature"] = (
        dfm_sm["Feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )

    # sort descending so largest effects appear first
    dfm_sm = dfm_sm.sort_values("Marginal Effect", ascending=False)

    st.subheader("5.2.1.3. Small Facility Marginal Effects Interpretation")
    st.markdown("""
    Below (see **Tale: 9**) is the full table of average marginal revenue uplifts per 1-unit increase, capturing both nonlinear and interaction effects learned by our Small Facility Random Forest.
    """)

    # display as a scrollable DataFrame
    st.dataframe(
        dfm_sm.set_index("Feature")
            .style.format({"Marginal Effect":"${:,.2f}"}),
        use_container_width=False,
        height=400
    )
    st.caption("**Table 9:** Marginal Effects (per 1-unit increase) for Small Facility Random Forest")

    # OLS-style write-up for the top two
    f1, v1 = dfm_sm.iloc[0][["Feature","Marginal Effect"]]
    f2, v2 = dfm_sm.iloc[1][["Feature","Marginal Effect"]]

    st.markdown(f"""
    Our model suggests that none of the Small Facility marketing channels or interactions deliver a significant standalone revenue uplift. Infact, YouTube and Instagram have negative marginal effects, indicating that increasing their activity would actually reduce revenue.
    """)

    mets_med = json.load(open("Outputs/segments/rf_metrics_Medium_Facility.json"))

    st.subheader("5.2.2.1. Medium Facility Random Forest Results and Interpretation")
    st.markdown(f"""
    Next, let's focus on the Medium Facility, we trained a Random Forest (200 trees, same eight marketing channels plus all pairwise interactions) to predict `Amount_Collected`. This model delivers a Test RMSE of {mets_med['rmse']:.0f}, reflecting the typical revenue deviation, and explains {mets_med['r2']:.1%} of the out-of-sample variance. Its average 5-fold CV R² of {mets_med['avg_cv_r2']:.3f} underscores consistent predictive strength across folds.
    """)

    # 5.4.2 Medium Facility Top Predictors (Feature Importances)
    st.subheader("5.2.2.2. Medium Facility Top Predictors (Feature Importances)")

    st.markdown("""
    **Table 10** and **Figure 20** summarize the five most influential features in our Medium Facility Random Forest model. Importance values reflect each variable’s average contribution to reducing out-of-sample error across all trees.

    - **Instagram (0.233):** The leading standalone driver—medium-scale operations see the greatest uplift per unit of Instagram activity.  
    - **Campaign Flyer × Instagram (0.170):** Integrating traditional flyers with Instagram amplifies campaign effectiveness.  
    - **YouTube (0.140):** A strong secondary channel, highlighting the value of video content.  
    - **Facebook × Instagram (0.110):** Cross-platform social strategies deliver meaningful revenue gains.  
    - **Campaign Flyer × Facebook (0.092):** Print and Facebook synergy still matters at moderate scale.
    """)

    # load and display table
    fi_med = pd.read_csv("Outputs/segments/feature_importance_Medium_Facility.csv")
    fi_med["Feature"] = (
        fi_med["feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    fi_med_display = (
        fi_med[["Feature","importance"]]
        .rename(columns={"importance":"Importance"})
    )

    st.dataframe(
        fi_med_display.head(5).style.format({"Importance":"{:.3f}"}),
        use_container_width=False,
        height=250
    )
    st.caption("**Table 10:** Top 5 Feature Importances from the Medium Facility Random Forest")

    # bar chart
    fig = px.bar(
        fi_med_display.head(5)[::-1],
        x="Importance", y="Feature",
        orientation="h",
        text="Importance",
        labels={"Importance":"Importance","Feature":"Feature"},
        title="Medium Facility – Top 5 Feature Importances",
        color_discrete_sequence=["#1A5632"]
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(
        margin=dict(l=150, r=20, t=50, b=20),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure 20: Top 5 Feature Importances from the Medium Facility Random Forest")

    # 5.4.3 Medium Facility Marginal Effects Interpretation
    st.subheader("5.2.2.3. Medium Facility Marginal Effects Interpretation")

    st.markdown("""
    Below (see **Table 11**) is the full table of average marginal revenue uplifts per 1-unit increase, capturing both non-linear and interaction effects learned by our Medium Facility Random Forest.
    """)

    # load and display marginals
    marg_med = json.load(open("Outputs/segments/rf_marginals_Medium_Facility.json"))
    dfm_med = (
        pd.DataFrame.from_dict(marg_med, orient="index", columns=["Marginal Effect"])
        .reset_index()
        .rename(columns={"index":"Feature"})
    )
    dfm_med["Feature"] = (
        dfm_med["Feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    dfm_med = dfm_med.sort_values("Marginal Effect", ascending=False)

    st.dataframe(
        dfm_med.set_index("Feature").style.format({"Marginal Effect":"${:,.2f}"}),
        use_container_width=False,
        height=400
    )
    st.caption("**Table 11:** Marginal Effects (per 1-unit increase) for Medium Facility Random Forest")

    # OLS-style write-up for the top two
    f1, v1 = dfm_med.iloc[0][["Feature","Marginal Effect"]]
    f2, v2 = dfm_med.iloc[1][["Feature","Marginal Effect"]]

    st.markdown(f"""
    A one-unit increase in {f1} is associated with an average uplift of \${v1:,.2f}, while a one-unit increase in {f2} yields about ${v2:,.2f}, holding all else constant.
    """)

    # 5.4.3 Private Facility Random Forest Results and Interpretation
    mets_priv = json.load(open("Outputs/segments/rf_metrics_Private_Facility.json"))

    # 5.4.4 Large Facility Random Forest Results and Interpretation
    mets_large = json.load(open("Outputs/segments/rf_metrics_Large_Facility.json"))

    st.subheader("5.2.3.1. Private Facility Random Forest Results and Interpretation")
    st.markdown(f"""
    For Private Facilities, our Random Forest— achieves a Test RMSE of {mets_priv['rmse']:.0f}, indicating the model’s average error in dollars. It captures {mets_priv['r2']:.1%} of the revenue variation out of sample, and its average 5-fold CV R² of {mets_priv['avg_cv_r2']:.3f} demonstrates robust generalization despite the smaller sample size.
    """)

    # 5.4.4 Private Facility Top Predictors (Feature Importances)
    st.subheader("5.2.3.2. Private Facility Top Predictors (Feature Importances)")

    st.markdown("""
    **Table 12** and **Figure 21** summarize the five most influential features in our Private Facility Random Forest model. Importance values reflect each variable’s average contribution to reducing out-of-sample error across all trees.

    - **Instagram (0.683):** The dominant driver—private operators gain the largest revenue lift per unit of Instagram activity.  
    - **Campaign Flyer (0.123):** Traditional outreach remains a solid standalone driver in this segment.  
    - **Campaign Flyer × Instagram (0.103):** Pairing flyers with Instagram provides additional uplift beyond each alone.  
    - **YouTube (0.048):** Video content yields modest but meaningful gains.  
    - **Instagram × YouTube (0.028):** Synergies between video platforms contribute incremental value.
    """)

    fi_priv = pd.read_csv("Outputs/segments/feature_importance_Private_Facility.csv")
    fi_priv["Feature"] = (
        fi_priv["feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    fi_priv_disp = fi_priv[["Feature","importance"]].rename(columns={"importance":"Importance"})

    st.dataframe(
        fi_priv_disp.head(5).style.format({"Importance":"{:.3f}"}),
        use_container_width=False,
        height=250
    )
    st.caption("**Table 12:** Top 5 Feature Importances from the Private Facility Random Forest")

    fig = px.bar(
        fi_priv_disp.head(5)[::-1],
        x="Importance", y="Feature",
        orientation="h",
        text="Importance",
        labels={"Importance":"Importance","Feature":"Feature"},
        title="Private Facility – Top 5 Feature Importances",
        color_discrete_sequence=["#1A5632"]
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(margin=dict(l=150, r=20, t=50, b=20), plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure 21: Top 5 Feature Importances from the Private Facility Random Forest")

    # 5.4.5 Private Facility Marginal Effects Interpretation
    st.subheader("5.2.3.3. Private Facility Marginal Effects Interpretation")

    st.markdown("""
    Below (see **Table 13**) is the full table of average marginal revenue uplifts per 1-unit increase, capturing both non-linear and interaction effects learned by our Private Facility Random Forest.
    """)

    marg_priv = json.load(open("Outputs/segments/rf_marginals_Private_Facility.json"))
    dfm_priv = (
        pd.DataFrame.from_dict(marg_priv, orient="index", columns=["Marginal Effect"])
        .reset_index().rename(columns={"index":"Feature"})
    )
    dfm_priv["Feature"] = (
        dfm_priv["Feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    dfm_priv = dfm_priv.sort_values("Marginal Effect", ascending=False)

    st.dataframe(
        dfm_priv.set_index("Feature").style.format({"Marginal Effect":"${:,.2f}"}),
        use_container_width=False,
        height=400
    )
    st.caption("**Table 13:** Marginal Effects (per 1-unit increase) for Private Facility Random Forest")

    # OLS‐style write‐up for top two
    f1, v1 = dfm_priv.iloc[0][["Feature","Marginal Effect"]]
    f2, v2 = dfm_priv.iloc[1][["Feature","Marginal Effect"]]

    st.markdown(f"""
    Our model suggests that none of the Private Facility marketing channels or interactions deliver a significant standalone revenue uplift. Infact, YouTube and Instagram have negative marginal effects, indicating that increasing their activity would actually reduce revenue.
    """)
    st.subheader("5.2.4.1. Large Facility Random Forest Results and Interpretation")
    st.markdown(f"""
    For the Large Facilities, the Random Forest model yields a Test RMSE of {mets_large['rmse']:.0f}, showing its precision in predicting high-volume revenues.   This segment-specific model explains {mets_large['r2']:.1%} of the variance on held-out data, and its average 5-fold CV R² of {mets_large['avg_cv_r2']:.3f} highlights stable performance even with greater data complexity.
    """)
    # 5.4.6 Large Facility Top Predictors (Feature Importances)
    st.subheader("5.2.4.2. Large Facility Top Predictors (Feature Importances)")

    st.markdown("""
    **Table 14** and **Figure 22** detail the five most important features in our Large Facility Random Forest model. Importance values reflect each feature’s average role in reducing prediction error.

    - **Instagram (0.258):** A key driver even at scale, reflecting broad social engagement.  
    - **Instagram × YouTube (0.155):** Cross-platform video strategies deliver significant incremental returns.  
    - **Facebook × TikTok (0.119):** Social media pairings add meaningful lift for larger operations.  
    - **Campaign Flyer × Instagram (0.092):** Integrated print-to-social campaigns remain effective.  
    - **TikTok (0.085):** A strong standalone channel for reaching younger demographics.
    """)

    fi_large = pd.read_csv("Outputs/segments/feature_importance_Large_Facility.csv")
    fi_large["Feature"] = (
        fi_large["feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    fi_large_disp = fi_large[["Feature","importance"]].rename(columns={"importance":"Importance"})

    st.dataframe(
        fi_large_disp.head(5).style.format({"Importance":"{:.3f}"}),
        use_container_width=False,
        height=250
    )
    st.caption("**Table 14:** Top 5 Feature Importances from the Large Facility Random Forest")

    fig = px.bar(
        fi_large_disp.head(5)[::-1],
        x="Importance", y="Feature",
        orientation="h",
        text="Importance",
        labels={"Importance":"Importance","Feature":"Feature"},
        title="Large Facility – Top 5 Feature Importances",
        color_discrete_sequence=["#1A5632"]
    )
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig.update_layout(margin=dict(l=150, r=20, t=50, b=20), plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Figure 22: Top 5 Feature Importances from the Large Facility Random Forest")

    # 5.4.7 Large Facility Marginal Effects Interpretation
    st.subheader("5.2.4.3. Large Facility Marginal Effects Interpretation")

    st.markdown("""
    Below is the full table of average marginal revenue uplifts per 1-unit increase, capturing both non-linear and interaction effects learned by our Large Facility Random Forest.
    """)

    marg_large = json.load(open("Outputs/segments/rf_marginals_Large_Facility.json"))
    dfm_large = (
        pd.DataFrame.from_dict(marg_large, orient="index", columns=["Marginal Effect"])
        .reset_index().rename(columns={"index":"Feature"})
    )
    dfm_large["Feature"] = (
        dfm_large["Feature"]
        .str.replace("_x_", " × ")
        .str.replace("_", " ")
        .str.title()
    )
    dfm_large = dfm_large.sort_values("Marginal Effect", ascending=False)

    st.dataframe(
        dfm_large.set_index("Feature").style.format({"Marginal Effect":"${:,.2f}"}),
        use_container_width=False,
        height=400
    )
    st.caption("**Table 14:** Marginal Effects (per 1-unit increase) for Large Facility Random Forest")

    # OLS‐style write‐up for top two
    f1, v1 = dfm_large.iloc[0][["Feature","Marginal Effect"]]
    f2, v2 = dfm_large.iloc[1][["Feature","Marginal Effect"]]

    st.markdown(f"""
    A one-unit increase in {f1} is associated with an average uplift of \${v1:,.2f}, while a one-unit increase in {f2} yields about ${v2:,.2f}, holding all else constant.
    """)

# 5.3. Summary of Random Forest Models
    st.subheader("5.3. Summary of Random Forest Models")

    st.markdown("""
    **Table 14** below compares the out-of-sample performance and top predictors for each Random Forest. The pooled model leads with the highest Test R², followed by Medium and Large Facility models. The Small Facility model shows solid performance driven by social media channels, while the Private Facility model exhibits a negative R², indicating poor fit—likely due to limited data variation. Across all models, Instagram and multi-channel interactions consistently rank among the top five predictors, with traditional flyers playing a larger role in larger segments.
    """)



    models = ["Pooled", "Small Facility", "Medium Facility", "Private Facility", "Large Facility"]
    rows = []

    for model in models:
        if model == "Pooled":
            mets = json.load(open("Outputs/rf_metrics.json"))
            fi   = pd.read_csv("Outputs/feature_importance.csv")
        else:
            safe = model.replace(" ", "_")
            mets = json.load(open(f"Outputs/segments/rf_metrics_{safe}.json"))
            fi   = pd.read_csv(f"Outputs/segments/feature_importance_{safe}.csv")
        fi["Feature"] = (
            fi["feature"]
            .str.replace("_x_", " × ")
            .str.replace("_", " ")
            .str.title()
        )
        top5 = fi.nlargest(5, "importance")["Feature"].tolist()
        rows.append({
            "Model": model,
            "Test RMSE": mets["rmse"],
            "Test R²": mets["r2"],
            "Avg CV R²": mets["avg_cv_r2"],
            "Top 5 Features": ", ".join(top5)
        })

    summary_df = pd.DataFrame(rows)
    # rank by Test R² descending
    summary_df["Rank"] = summary_df["Test R²"].rank(ascending=False, method="dense").astype(int)
    summary_df = summary_df.sort_values("Rank")

    # Display in Streamlit
    st.dataframe(
        summary_df[["Rank","Model","Test RMSE","Test R²","Avg CV R²","Top 5 Features"]]
        .style.format({
            "Test RMSE": "{:,.0f}",
            "Test R²":   "{:.3f}",
            "Avg CV R²": "{:.3f}"
        }),
        use_container_width=True,
        height=350
    )
    st.caption("**Table 15:** Diagnostics and top five predictors for each Random Forest model.")




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