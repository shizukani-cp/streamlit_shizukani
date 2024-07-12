import streamlit as st

from src.streamlit_shizukani.modules.main import main as responce


def break_markdown_links(text, max_length=48):
    words = text.split()
    result_lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) > max_length:
            result_lines.append(current_line)
            current_line = ""

        current_line += word + " "

    if current_line:
        result_lines.append(current_line)

    formatted_text = "  \n".join(result_lines)

    return formatted_text.strip()


if "history" not in tuple(st.session_state):
    st.session_state["history"] = ""

with st.form("my_form", clear_on_submit=True):
    text_place = st.empty()
    input_text = st.text_input("静カニに話したいことは？")
    submitted = st.form_submit_button("話す！")
    if submitted:
        st.session_state["history"] += f"あなた: {input_text}  \n"
        with st.spinner("考え中…"):
            responce_text = responce(input_text)
            breaked_text = break_markdown_links(responce_text)
        st.session_state["history"] += f"静カニ: {breaked_text}  \n"
    print(st.session_state["history"])
    text_place = text_place.write(st.session_state["history"])
