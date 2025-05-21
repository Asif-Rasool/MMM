import streamlit as st

st.set_page_config(
    page_title="EDA",
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
    st.header("3. Exploratory Data Analysis (EDA)")

    ### 2.2. Exploratory Data Analysis (EDA)

    st.markdown("""
    Our initial analysis focuses on understanding how sales vary across different types of businesses and levels of competition. This helps us begin to address our two key questions:  
    (1) how marketing campaigns impact sales, and  
    (2) whether the same strategy works across all types of businesses.

    #### Distribution by Client Type

    The dataset is dominated by **Large Facilities**, which make up about 46% of all records. **Small Facilities** follow at 28%, while **Medium** and **Private Facilities** represent smaller shares at 17% and 9%, respectively. This distribution informs how representative our insights will be across different segments (see **Figure 2**).
    """)
    st.image("Figures/client_type_distribution.png", width=400)
    st.caption("**Figure 2:** Proportion of records by Client Type based on normalized value counts.")

    st.markdown("""
    #### Competitive Environment Across Clients

    We then examined how competition is distributed across client types. Interestingly, all four client types (Large, Medium, Private, and Small Facilities) show the same proportion: **about 17% of businesses operate in a high-competition setting**, while **83% are in low-competition areas**. This consistency allows us to isolate competition effects without worrying about sample imbalance across categories (**Figure 3**).
    """)
    st.image("Figures/client_type_vs_competition_crosstab.png", width=700)
    st.caption("**Figure 3:** Crosstab of Client Type vs. Number of Competition (column-normalized).")

    st.markdown("""
    #### Sales vs. Competition

    Surprisingly, businesses in **high-competition areas** show a much higher average revenue, collecting nearly **$29.7 million**, compared to **$14.5 million** in low-competition regions. This challenges the intuitive assumption that more competition leads to lower sales. It may suggest that businesses in denser, more competitive environments are also in higher-demand markets or are more aggressive with marketing (see **Figure 4**).
    """)
    st.image("Figures/competition_vs_sales.png", width=700)
    st.caption("**Figure 4:** Average Amount Collected by Level of Competition.")

    st.markdown("""
    #### Sales by Client Type

    When comparing average sales across business types, **Medium Facilities** stand out with the highest average revenue, exceeding **$40 million**. **Large Facilities** follow with around **$20 million**, while **Private** and **Small Facilities** trail significantly. A similar trend appears in units sold, with Medium Facilities again outperforming the rest. These results suggest that business type plays a critical role in sales performance. Strategies likely need to be tailored accordingly — what works for a Medium Facility may not deliver the same results for a Small or Private one (**Figure 5**).
    """)
    st.image("Figures/client_type_vs_sales.png", width=700)
    st.caption("**Figure 5:** Mean Amount Collected and Units Sold by Client Type.")



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

