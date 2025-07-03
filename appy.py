import streamlit as st
import pandas as pd

st.title("Примерен App за зареждане на CSV файлове с изолинии")

# Зареждане на CSV файла с подходящи настройки
@st.cache_data
def load_fi_data():
    try:
        df = pd.read_csv("fi.csv", delimiter=';', encoding='utf-8')
    except UnicodeDecodeError:
        # Ако има проблем с utf-8, пробваме с latin1
        df = pd.read_csv("fi.csv", delimiter=';', encoding='latin1')
    return df

df_fi = load_fi_data()

st.subheader("Данни от fi.csv:")
st.dataframe(df_fi)

# Параметър Fi, който потребителят въвежда
fi_input = st.number_input("Въведи стойност на Fi:", value=0.0, step=0.1)

st.write(f"Въведена стойност Fi: {fi_input}")

# Примерна визуализация - може да добавиш още логика
st.line_chart(df_fi[['fi']])

# Тук можеш да добавиш следващата логика за обработка на данните
