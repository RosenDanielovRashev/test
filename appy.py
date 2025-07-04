import streamlit as st

st.title("Главна страница")

if st.button("Отиди към second_page"):
    st.switch_page("second_page")
