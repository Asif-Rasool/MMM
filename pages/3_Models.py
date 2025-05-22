import streamlit as st

st.set_page_config(
    page_title="Models",
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
    st.header("3. Modeling Strategy")
    st.markdown("""
    Our modeling strategy is based on the two primary goals of this project: first, to measure the impact of each marketing and social media campaign on sales, and second, to determine whether the same strategy is equally effective across different types of businesses.

    We begin with a linear regression model to establish a baseline. This model provides interpretable estimates of how each campaign input contributes to revenue outcomes. It is particularly useful in answering the first objective by quantifying marginal effects in a straightforward way.

    We then move to tree-based models, such as random forest and gradient boosting. These models allow for more complex relationships between variables, including non-linearities and interactions, which are likely present in real-world campaign behavior. They also provide a stronger basis for examining whether strategy effectiveness varies by business type.

    Model performance will be assessed using standard regression metrics, including R-squared, root mean squared error (RMSE), and mean absolute error (MAE).
    """)


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