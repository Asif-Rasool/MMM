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
    st.header("7. Recommendation")




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
    SYSTEM: You are Lion AI, a friendly virtual economist developed by Asif Rasool working with the Business Research Center at Southeastern Louisiana University.
    Use a conversational tone and Markdown formatting.

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

############################################################################################




import streamlit as st
import pandas as pd
from pathlib import Path

# ─── 1. Cache available summary files (excluding pooled model) ─────────────────
@st.cache_data
def list_summary_files(outputs_dir: str = "Outputs") -> dict[str, str]:
    p = Path(outputs_dir)
    files_map: dict[str, str] = {}
    for f in p.glob("*_summary.csv"):
        # Skip the pooled model summary
        if f.stem.startswith("pooled"):  
            continue
        # Remove the suffix for display
        display_name = f.stem.replace("_summary", "").rstrip("_")
        files_map[display_name] = f.name
    return files_map

# ─── 2. Cache loading a segment’s ROI estimates from CSV ───────────────────────
@st.cache_data
def load_segment_roi(filename: str, outputs_dir: str = "Outputs") -> pd.DataFrame:
    path = Path(outputs_dir) / filename
    df = pd.read_csv(path)
    # Keep only the coefficient column and rename
    df = df[["Variable", "Coefficient (Impact)"]].copy()
    df.columns = ["Channel", "Per Dollar ROI"]
    df.set_index("Channel", inplace=True)
    return df

# ─── 3. Streamlit UI ─────────────────────────────────────────────────────────
st.header("Per-Dollar ROI by Channel")

# Main app function

def main():
    files_map = list_summary_files()
    choice = st.selectbox("Select client segment", list(files_map.keys()))

    # Load and display the ROI table
    roi_df = load_segment_roi(files_map[choice])
    st.subheader(f"{choice} Segment ROI")
    st.dataframe(roi_df, use_container_width=True)

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