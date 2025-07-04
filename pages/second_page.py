import streamlit as st

st.title("Втора Страница")
st.write("Това е втората страница!")
if st.button("Обратно към началото"):
    st.switch_page("app.py")  # Връщане към главния файл
