import streamlit as st

st.title("Главна страница")

st.write("Налични страници:")
for page in st._runtime._session_state._pages.keys():
    st.write("-", page)

if st.button("Отиди към second_page"):
    st.switch_page("second_page")
