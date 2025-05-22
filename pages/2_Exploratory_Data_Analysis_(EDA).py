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

    st.markdown("""
    
    Our initial analysis focuses on understanding how sales vary across different types of businesses and levels of competition. This helps us begin to address our two key questions:  
    (1) how marketing campaigns impact sales, and  
    (2) whether the same strategy works across all types of businesses.
    """)
    st.subheader("3.1. Distribution Analysis")
    st.subheader("3.1.1. Distribution by Client Type")
    st.markdown("""
    The dataset is dominated by **Large Facilities**, which make up about 46% of all records. **Small Facilities** follow at 28%, while **Medium** and **Private Facilities** represent smaller shares at 17% and 9%, respectively. This distribution informs how representative our insights will be across different segments (see **Figure 2**).
    """)
    st.image("Figures/client_type_distribution.png", width=320)
    st.caption("**Figure 2:** Proportion of records by Client Type based on normalized value counts.")

    st.subheader("3.1.2. Competitive Environment Across Clients")
    st.markdown("""
    We then examined how competition is distributed across client types. Interestingly, all four client types (Large, Medium, Private, and Small Facilities) show the same proportion: **about 17% of businesses operate in a high-competition setting**, while **83% are in low-competition areas**. This consistency allows us to isolate competition effects without worrying about sample imbalance across categories (**Figure 3**).
    """)
    st.image("Figures/client_type_vs_competition_crosstab.png", width=700)
    st.caption("**Figure 3:** Crosstab of Client Type vs. Number of Competition (column-normalized).")

    st.subheader("3.1.3. Sales vs. Competition")
    st.markdown("""
    Surprisingly, businesses in **high-competition areas** show a much higher average revenue, collecting nearly **\$29.7 million**, compared to **$14.5 million** in low-competition regions. This challenges the intuitive assumption that more competition leads to lower sales. It may suggest that businesses in denser, more competitive environments are also in higher-demand markets or are more aggressive with marketing (see **Figure 4**).
    """)
    st.image("Figures/competition_vs_sales.png", width=520)
    st.caption("**Figure 4:** Average Amount Collected by Level of Competition.")

    st.subheader("3.1.4. Sales by Client Type")
    st.markdown("""
    When comparing average sales across business types, **Medium Facilities** stand out with the highest average revenue, exceeding **\$40 million**. **Large Facilities** follow with around **$20 million**, while **Private** and **Small Facilities** trail significantly. A similar trend appears in units sold, with Medium Facilities again outperforming the rest. These results suggest that business size plays a critical role in sales performance. Strategies likely need to be tailored accordingly — what works for a Medium Facility may not deliver the same results for a Small or Private one (**Figure 5**).
    """)
    st.image("Figures/client_type_vs_sales.png", width=520)
    st.caption("**Figure 5:** Mean Amount Collected and Units Sold by Client Type.")

    st.subheader("3.2. Correlation Analysis")
    st.subheader("3.2.1. Identifying Linear Relationships with Sales")
    st.markdown("""

To inform a consolidated strategy for targeting, we examined how individual campaign types and social media platforms correlate with revenue. This helps us identify which inputs are more linearly associated with total sales, and may warrant more investment or closer analysis.

We calculated Pearson correlation coefficients between `Amount_Collected` and various campaign-related variables. These coefficients capture the degree of linear association between each input and revenue.

The ranked figure below (**Figure 6**) highlights which campaign or platform variables are more strongly correlated with sales.


""")
    
    st.image("Figures/correlation_analysis.png", width=500)
    st.caption("**Figure 6:** Correlation of different campaign and platform variables with total revenue collected.")

    st.subheader("3.2.2. Segment-Specific Correlation Analysis: Do Different Business Types Respond to Campaigns Differently?")
    st.markdown("""
To identify which marketing strategies are more effective for different business types, we computed the correlation between `Amount_Collected` and various campaign/platform variables, separately for each **Client Type**.

The heatmap below (**Figure 7**) shows how strongly each variable is associated with revenue for Large, Medium, Private, and Small Facilities. Darker shades indicate stronger positive correlations.

Some clear patterns emerge:

- **Instagram consistently shows the strongest positive correlation across all segments**, especially for Medium and Private Facilities.
- **Campaign_Flyer** and **Facebook** perform well for Large and Medium Facilities, but have little impact for smaller clients.
- **TikTok and YouTube** show weak to moderate effects, depending on the segment.
- **Phone-based campaigns and LinkedIn** appear to have minimal or even negative associations with sales.

We can see that. a one-size-fits-all campaign could miss opportunities—or waste resources—depending on the business type.
""")
    st.image("Figures/segmented_correlation_heatmap.png", width=700)
    st.caption("**Figure 7:** Correlation heatmap showing how campaign and platform variables relate to revenue, segmented by Client Type.")

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

