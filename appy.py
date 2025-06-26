import streamlit as st

if "step" not in st.session_state:
    st.session_state.step = 1

def next_step():
    st.session_state.step += 1

st.title("Многоетапно приложение")

if st.session_state.step == 1:
    st.subheader("Стъпка 1: Въведи твоето име")
    name = st.text_input("Име:")
    if st.button("Напред"):
        if name.strip() != "":
            st.session_state.name = name
            next_step()
        else:
            st.warning("Моля, въведи име!")

elif st.session_state.step == 2:
    st.subheader("Стъпка 2: Въведи възраст")
    age = st.number_input("Възраст:", min_value=0, step=1)
    if st.button("Напред"):
        st.session_state.age = age
        next_step()

elif st.session_state.step == 3:
    st.subheader("Готово! Обобщение:")
    st.write(f"👤 Име: {st.session_state.name}")
    st.write(f"🎂 Възраст: {st.session_state.age}")
    if st.button("Започни отначало"):
        st.session_state.step = 1

