import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation

st.set_page_config(page_title="MLSAC Plot Gallery", layout="wide")

# Initialize a "database" in the app's memory to store submissions
if "gallery_data" not in st.session_state:
    st.session_state.gallery_data = []

st.title("🎨 The MLSAC Eidreat Plot Gallery ✨")
tab1, tab2 = st.tabs(["📤 Submit Your Plot", "🖼️ View Gallery"])

# --- TAB 1: SUBMISSION ---
with tab1:
    st.header("Create your Plot: 🖌️🎨")
    name = st.text_input("Your Name / Autograph", placeholder="e.g., your name (dep. name)")
    user_code = st.text_area("Paste your Python/Matplotlib code here", height=200, 
                             placeholder="import matplotlib.pyplot as plt\nfig, ax = plt.subplots()...")

    if st.button("Submit to Gallery"):
        if name and user_code:
            # We create the plot immediately to 'test' it and save the figure
            try:
                # Use a local namespace for execution safety
                local_vars = {}
                exec(user_code, {"plt": plt, "pd": pd, "np": np}, local_vars)
                fig = plt.gcf()
                
                # Save to our session gallery
                st.session_state.gallery_data.append({
                    "name": name,
                    "code": user_code,
                    "fig": fig
                })
                st.success("Successfully added to the gallery!")
            except Exception as e:
                st.error(f"Error in code: {e}")

# --- TAB 2: THE GALLERY ---
with tab2:
    st.header("The Gallery")
    if not st.session_state.gallery_data:
        st.info("No submissions yet. Be the first!")
    else:
        # Create a grid of thumbnails (3 columns)
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.gallery_data):
            with cols[idx % 3]:
                # Show the thumbnail
                st.pyplot(item['fig'])
                if st.button(f"View {item['name']}'s Code", key=f"btn_{idx}"):
                    # When clicked, show the code and the "Autograph"
                    st.markdown(f"**Artist:** {item['name']}")
                    st.code(item['code'], language='python')
                    st.divider()
