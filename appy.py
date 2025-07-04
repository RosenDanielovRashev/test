# main_app.py
import streamlit as st

st.title("Главна страница")

st.write("Натисни бутона, за да отидеш на втората страница.")

if st.button("Отиди"):
    st.switch_page("Втора страница")
