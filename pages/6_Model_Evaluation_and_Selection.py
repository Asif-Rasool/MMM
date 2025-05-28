import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json

st.set_page_config(
    page_title="Model Evaluation and Selection",
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
    st.header("6. Model Evaluation and Selection")

    st.markdown("""
    
    To identify the best model, we held out 20 % of our data for out-of-sample testing and trained two families of models—ordinary least squares (OLS) and Random Forests—on both the pooled sample and on each business segment (Small, Medium, Large and Private facilities).

    For every model, we computed a rich set of diagnostics on the test set:
    - **RMSE** (root mean squared error) and **MSE** to measure average prediction error  
    - **MAE** (mean absolute error) and **MAPE** (mean absolute percentage error) for scaled error insights  
    - **R²** and **adjusted R²** to quantify explained variance  
    - **Explained variance**, **SSE** and **TSS** to decompose total versus residual variance  
    - **5-fold CV R²** for cross-validated stability  
    - **Fit time** to gauge computational cost  

    We then ranked all ten models by their test R² (higher is better) and flagged the top performer. By combining rigorous out-of-sample metrics with cross-validation and computational efficiency, we ensure our final recommendation balances accuracy, generalizability, and practicality.

    Below (**Table 16**), we present the concise comparison of key metrics and model ranks. 
    """)



# --- 1) Build the comparison DataFrame ---------------------------------
# You can also load this from your saved JSONs, but here’s the manual version:

    data = {
        "Model": [
            "RF (Pooled)", "RF – Medium Facility", "RF – Large Facility",
            "OLS (Pooled)", "RF – Small Facility", "RF – Private Facility",
            "OLS – Medium Facility", "OLS – Small Facility",
            "OLS – Large Facility", "OLS – Private Facility"
        ],
        "Rank":           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "RMSE":           [29103805, 38729247, 21835655, 31933998,
                          6346458, 17522766, 91891416, 11055522,
                          66248547, 71453333468472754176],
        "MSE":            [8.47e14, 1.50e15, 4.77e14, 1.02e15,
                          4.03e13, 3.07e14, 8.44e15, 1.22e14,
                          4.39e15, 5.11e39],
        "MAE":            [20507648, 29684798, 15709003, 21220011,
                          4621793, 13508832, 45574735, 6915888,
                          20270661, 19096706641575051264],
        "MAPE (%)":       [100.0, 100.0, 100.0, 100.0,
                          89.0, 100.0, 100.0, 100.0,
                          100.0, 100.0],
        "R\u00b2":         [ 0.368,  0.365,  0.240,  0.239,
                          -0.370, -1.000, -1.000, -3.157,
                          -5.999, -1.000],
        "Adj. R\u00b2":    [ 0.284, -0.132,  0.048,  0.138,
                            1.000,  1.000, -1.000,  1.000,
                          -1.000,  1.000],
        "Avg CV R\u00b2":  [ 0.417,  0.413,  0.272, -0.229,
                          -0.092, -0.248, -3.475, -0.371,
                            0.078, -1.000],
        "🏆":              ["✔", "", "", "", "", "", "", "", "", ""]
    }

    df_compare = pd.DataFrame(data).set_index("Model")

# assume df_compare is your DataFrame from before, with the raw ints/floats
    df_disp = df_compare.copy()

    # 1) Define your string formats
    fmt_map = {
        "RMSE":            "{:,.0f}",
        "MSE":             "{:.2e}",
        "MAE":             "{:,.0f}",
        "MAPE (%)":        "{:.1f}%",
        "R\u00b2":          "{:.3f}",
        "Adj. R\u00b2":     "{:.3f}",
        "Avg CV R\u00b2":   "{:.3f}"
    }

    # 2) Apply them to each column (converting to string dtype)
    for col, fmt in fmt_map.items():
        df_disp[col] = df_disp[col].map(lambda x: fmt.format(x))

    # Rank & Recommendation can stay as-is (they're already small ints / short strings)

    # 3) Render
    
    st.dataframe(
        df_disp.reset_index()
              .rename(columns={"index":"Model"}),
        use_container_width=True
    )
    st.caption("**Table 16:** Key diagnostics, ranked by Test R², with the selected model flagged.")

    st.markdown("""
The pooled Random Forest achieves the best balance of accuracy (lowest RMSE & highest R²) and stability (strong cross-validated R²), earning the ✔ selection mark Segment-specific OLS variants exhibit wildly unstable R² (often < 0) and are not recommended, whereas Random Forests trained per segment generally outperform their OLS counterparts. Overall, the pooled Random Forest model delivers the most reliable uplift estimates for our marketing recommendations.
""")
    
    # Immediately after your comparison table & explanatory text...

    st.markdown("""
**While the pooled Random Forest outperformed OLS on standard accuracy metrics, we observed several implausible uplift estimates—an artifact of our synthetic data. To ensure our recommendation engine is grounded in realistic, interpretable effects, we will base our final marketing uplift recommendations on the OLS coefficient estimates for this prototype, even though RF achieved higher R² and lower RMSE.**
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