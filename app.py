import streamlit as st
from src.streamlit_shizukani.modules.main import main as responce

if "history" not in tuple(st.session_state):
    st.session_state["history"] = ""

with st.form("my_form", clear_on_submit=True):
    input_text = st.text_input("静カニに話したいことは？")
    submitted = st.form_submit_button("話す！")
    if submitted:
        st.session_state["history"] += f"あなた: {input_text}\n"
        with st.spinner("考え中…"):
            responce_text = responce(input_text)
            breaked_text = ""
            for i in range(0, len(responce_text), 48):
                breaked_text += f"{responce_text[i:i+48]}\n"
        st.session_state["history"] += f"静カニ: {breaked_text}\n"
    text = st.text(st.session_state["history"])