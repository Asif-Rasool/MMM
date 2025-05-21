import streamlit as st

import streamlit as st

st.set_page_config(
    page_title="Background",
    layout="wide",
    page_icon="athletic-logo-spirit-mark.svg",
    menu_items={
      'Get Help': None,
      'Report a bug': None,
      'About': None
    }
)


# ── 3‑COL LAYOUT ──
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.title("Signals and Sales: Modeling Social Media ROI for Northshore Businesses (prototype version)")
    with st.expander("About", expanded=False):

# Author Info
      st.markdown("""
Developed by Asif Rasool<sup>*</sup>, Ph.D. <a href="mailto:asif.rasool@southeastern.edu">📧</a> 

> Business Research Center, College of Business, Southeastern Louisiana University, 1514 Martens Drive, Hammond, LA 70401, USA  

""", unsafe_allow_html=True)

# Citation
      st.markdown("""
> Last update: 20 May, 2025

>(This model belongs to **Business Research Center, College of Business, Southeastern Louisiana University**)

>*To whom correspondence should be addressed
                    """)
with col2:
  st.markdown("---")
  st.header("1. Background")
  # st.markdown("---")
  st.markdown("""

The Northshore region has seen steady growth in its small business sector over the past decade. But for many of these businesses, finding and reaching the right audience remains a challenge. Marketing budgets are limited, digital ad platforms are complex, and most owners don’t have time to experiment or optimize.

At the same time, the way consumers make decisions has changed. Social media now plays a central role in how people discover, evaluate, and choose businesses—across sectors like retail, dining, health, and services. Despite this, many local campaigns underperform or fail to connect with the right audience.

This project introduces a model designed to help Northshore businesses run smarter, more effective ad campaigns—primarily through social media, but also other channels where appropriate. It evaluates what’s working, what’s not, and provides a strategy to maximize return on investment.

There are two core objectives of this project  
1. **To measure the impact of each marketing and social media campaign on actual sales** — measured through the dollar amount collected.  
2. **To determine whether the same strategy works across different types of businesses**, or whether tailored approaches are needed depending on industry, size, or customer base.

Developed by Dr. Asif Rasool, Research Economist at the **Business Research Center** in the **College of Business at Southeastern Louisiana University**, this model blends local economic data with ad performance insights to guide better marketing decisions. It offers a targeted, data-informed approach rather than a one-size-fits-all solution.

At its core, this work supports economic development. Helping small businesses reach more customers means stronger revenues, job creation, and a more resilient local economy. For a growing region like Northshore, that kind of support can make a measurable difference.
""")
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
