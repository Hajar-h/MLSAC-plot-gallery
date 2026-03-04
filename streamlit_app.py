import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(page_title="MLSAC Plot Gallery", layout="wide")

# Initialize a "database" in the app's memory to store submissions
if "gallery_data" not in st.session_state:
    st.session_state.gallery_data = []

st.title("🎨 The MLSAC Eidreat Plot Gallery ✨")
tab1, tab2 = st.tabs(["📤 Submit Your Plot", "🖼️ View Gallery"])

# --- TAB 1: SUBMISSION ---
with tab1:
    st.header("Share your creation")
    name = st.text_input("Your Name / Autograph")
    user_code = st.text_area("Paste your Python code here", height=250)

    if st.button("Submit to Gallery"):
        if name and user_code:
            try:
                # We create a shared dictionary for both globals and locals
                namespace = {
                    "plt": plt, 
                    "pd": pd, 
                    "np": np, 
                    "arabic_reshaper": arabic_reshaper,
                    "get_display": get_display
                }
                
                # We execute the code within that single namespace
                exec(user_code, namespace, namespace) 
                
                fig = plt.gcf()
                
                st.session_state.gallery_data.append({
                    "name": name,
                    "code": user_code,
                    "fig": fig
                })
                st.success("Successfully added!")
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
