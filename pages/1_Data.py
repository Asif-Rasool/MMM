import streamlit as st

st.set_page_config(
    page_title="Data",
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
  st.header("2. Data")
  
  st.markdown("""
We have created a synthetic dataset for model building, interpretation, and recommendation purposes. The idea is that once we have these models running, we can present their structure and performance to stakeholders. This will help motivate participation in the data collection process, which in turn will provide us with real data to rebuild our models, interpret results, and offer customized recommendations.

Eventually, we plan to deploy these models with a simple GUI, so that Northshore businesses can have a powerful tool at hand to run their marketing and social media campaigns. The models, once built on real data, will be paired with an easy-to-understand interface and provide clear recommendations to help businesses tailor their marketing strategies.
""")
  
col1, col2, col3 = st.columns([1, 6, 1])

with col2:

  st.subheader("2.1. Dataset Overview")
  st.markdown("""
  This synthetic dataset simulates marketing activity and sales performance for businesses in the Northshore region. Each row represents a monthly record of a specific business, capturing customer volume, campaign exposure, platform usage, and resulting sales. Below is a brief description of each variable (see **Figure 1** for a sample snapshot):

  - **Client_ID**: Unique identifier assigned to each business.  
  - **Client_Type**: Categorical classification of the business (e.g., Medium Facility).  
  - **Number_of_Customers**: Approximate number of customers associated with the business during the reporting period.  
  - **Monthly_Target**: Internal monthly sales or outreach target set by the business.  
  - **Zip_Code**: Geographic location identifier.  
  - **Calendardate**: Date of the record (monthly frequency).  
  - **Amount_Collected**: Total revenue (in dollars) collected during the month.  
  - **Unit_Sold**: Number of units or services sold.  
  - **Campaign_Email / Campaign_Flyer / Campaign_Phone**: Amount spent on each campaign type during the month, allowing us to assess the cost-effectiveness of different outreach methods.  
  - **Facebook / Instagram / YouTube / TikTok / LinkedIn**: Amount spent (or reach achieved) on each platform—used to model platform-specific impact.  
  - **Number_of_Competition**: Categorical variable reflecting the local business environment (e.g., Low, Medium, High competition).
  """)

  st.image("Figures/data_table.png", use_container_width=True)

  st.caption("**Figure 1:** Sample of the synthetic dataset showing monthly campaign activity and business performance across multiple platforms.")

  import pandas as pd

  # Load your data
  df_cleaned = pd.read_csv("Data/Campaign-Data.csv")  # Update path as needed

  # Add download button
  csv_data = df_cleaned.to_csv(index=False).encode('utf-8')
  st.download_button(
      label="📥 Download Synthetic Data",
      data=csv_data,
      file_name="synthetic_campaign_data.csv",
      mime="text/csv"
  )

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