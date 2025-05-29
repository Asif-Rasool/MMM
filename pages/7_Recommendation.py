import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import json
import streamlit as st

from pathlib import Path

st.set_page_config(
    page_title="Recommendation",
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
    st.header("Recommendation System")


import streamlit as st
import json
import tempfile
import os
from langchain.schema import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


# ── SESSION STATE INIT ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── GEMINI (Vertex AI) AUTH & MODEL SETUP ──────────────────────────────────────
@st.cache_resource
def init_lion_ai():
    creds = json.loads(st.secrets.google.credentials)
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as tf:
        json.dump(creds, tf)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = tf.name
    os.environ["GOOGLE_CLOUD_PROJECT"] = st.secrets.google.project_id
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
    os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2,
        callbacks=[StreamingStdOutCallbackHandler()],
        streaming=True,
    )

lion_ai = init_lion_ai()

@st.cache_data(ttl=3600)
def generate_lion_response(user_input: str) -> str:
    prompt = f"""
    SYSTEM: You are Lion AI, a virtual economist developed by Asif Rasool working with the Business Research Center at Southeastern Louisiana University.
    

    USER: {user_input}
    ASSISTANT:
    """
    msg = HumanMessage(content=prompt.strip())
    resp = lion_ai.invoke([msg])
    return resp.content


# ── SIDEBAR CHAT ────────────────────────────────────────────────────────────────
with st.sidebar.expander("💬 Chat with Lion AI", expanded=False):
    for chat in st.session_state.messages:
        role = "assistant" if chat["role"] == "assistant" else "user"
        avatar = "🦁" if role == "assistant" else None
        st.chat_message(role, avatar=avatar).write(chat["content"])

    user_input = st.chat_input("Type your message…", key="chat_input")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        reply = generate_lion_response(user_input)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()


####################################################################M
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

with col2:
    # ─── 1. Cache available summary files (excluding pooled model) ─────────────────
    @st.cache_data
    def list_summary_files(outputs_dir: str = "Outputs") -> dict[str, str]:
        p = Path(outputs_dir)
        files_map: dict[str, str] = {}
        for f in p.glob("*_summary.csv"):
            if f.stem.startswith("pooled"):  # skip pooled model summary
                continue
            base_name = f.stem.replace("_summary", "")
            display_name = base_name.replace("_", " ").strip()
            files_map[display_name] = f.name
        return files_map

    # ─── 2. Cache loading a segment’s ROI estimates from CSV ───────────────────────
    @st.cache_data
    def load_segment_roi(filename: str, outputs_dir: str = "Outputs") -> pd.DataFrame:
        path = Path(outputs_dir) / filename
        df = pd.read_csv(path)
        df = df[["Variable", "Coefficient (Impact)"]].copy()
        df.columns = ["Channel", "Per Dollar ROI"]
        df.set_index("Channel", inplace=True)
        return df

    # ─── 3. Streamlit UI ─────────────────────────────────────────────────────────
    st.markdown("---")
    
    st.subheader("Per-Dollar ROI by Channel")

    def main():
        # load business sizes
        files_map = list_summary_files()
        choice = st.selectbox("**Select Business Size**", list(files_map.keys()))

        # load and filter ROI data
        roi_df = load_segment_roi(files_map[choice])
        pos_df = (
            roi_df[roi_df["Per Dollar ROI"] > 0]
            .sort_values("Per Dollar ROI", ascending=False)
        )

        # plot bar chart
        fig = px.bar(
            pos_df.reset_index(),
            x="Channel",
            y="Per Dollar ROI",
            title=f"{choice} Top Positive ROI by Channel",
            color_discrete_sequence=["#1A5632"]
        )
        fig.update_layout(height=350, margin=dict(l=40, r=40, t=40, b=40))
        st.plotly_chart(fig, use_container_width=True)

        # show ROI table
        st.subheader(f"{choice} Segment Top Positive ROI Channels")
        st.table(pos_df)

        # ─── 4. Custom Campaign ROI Calculator ──────────────────────────────────────
        st.markdown("---")
        st.subheader("Run Custom Marketing Campaign")

        budget = st.number_input(
            "**Total Marketing Budget ($)**",
            min_value=0.0,
            value=100000.0,
            step=1000.0,
            format="%.2f"
        )

        channels = st.multiselect(
            "Select Channels to Include", pos_df.index.tolist(),
            default=pos_df.index.tolist()
        )

        if channels:
            # equal default allocation
            default_pct = 1.0 / len(channels)
            allocations = {}
            for ch in channels:
                pct = st.number_input(
                    f"Allocation % for {ch}",
                    min_value=0.0,
                    max_value=100.0,
                    value=round(default_pct * 100, 2),
                    step=1.0,
                    format="%.2f"
                ) / 100.0
                allocations[ch] = pct

            # warning if total allocation != 100%
            total_pct = sum(allocations.values())
            if abs(total_pct - 1.0) > 1e-2:
                st.warning("Allocations do not sum to 100%. Using entered values.")

            # calculate ROI only for channels with allocation > 0
            results = []
            for ch, pct in allocations.items():
                if pct <= 0:
                    continue
                allocated = budget * pct
                roi = float(pos_df.loc[ch, "Per Dollar ROI"])
                total = allocated * roi
                results.append({
                    "Channel": ch,
                    "Allocation %": pct * 100,
                    "Allocated Budget ($)": allocated,
                    "Per Dollar ROI": roi,
                    "Total ROI ($)": total,
                })
            results_df = pd.DataFrame(results).set_index("Channel").round(2)

            # add a total ROI summary row
            total_sum = results_df["Total ROI ($)"].sum()
            total_row = pd.DataFrame({col: [""] for col in results_df.columns}, index=["Total"])
            total_row.loc["Total", "Total ROI ($)"] = round(total_sum, 2)
            display_df = pd.concat([results_df, total_row])

            st.subheader("Custom Campaign ROI Results")
            st.table(display_df)

            #######################################################################################Report

        # Button to trigger Lion AI analysis
        if st.button("Get AI Insights from Lion AI"):
            # Show a spinner while waiting for the AI response
            with st.spinner("Generating insights with Lion AI..."):
                # Convert the two tables to markdown
                per_dollar_md = pos_df.reset_index().to_markdown(index=False)
                custom_md     = display_df.reset_index().to_markdown(index=False)

                # Build a single prompt for both tables
                prompt = f"""
        You are Lion AI, a virtual PhD economist. Analyze these two tables and provide:
        1. A summary of the per-dollar ROI by channel.
        2. Commentary on the custom campaign allocations.
        3. Recommendations on how to optimize budget allocation next time.

        **Per-Dollar ROI by Channel**  
        {per_dollar_md}

        **Custom Campaign ROI Results**  
        {custom_md}
        

        """

                # Call your existing function
                analysis = generate_lion_response(prompt)

            # Display the AI’s write-up
            st.subheader("Lion AI Insights")
            st.write(analysis)

            st.markdown(
        "<p style='font-size:0.85em;'><em>"
        "Lion AI is still in experimental phase – please consult with "
        "Asif Rasool before using this report "
        "(<a href='mailto:asif.rasool@southeastern.edu'>asif.rasool@southeastern.edu</a>)."
        "</em></p>",
        unsafe_allow_html=True,
    )
    if __name__ == "__main__":
            main()



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