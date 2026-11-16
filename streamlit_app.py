import streamlit as st
from llm import generate_shopping_list

st.set_page_config(page_title="Список покупок по блюду", page_icon="🍳")
st.title("🍳 Список покупок по блюду")
st.caption("Введите блюдо, выберите количество человек и формат ответа.")

with st.form("input_form"):
    dish = st.text_area("Что приготовить?", placeholder="Например: Паста карбонара", height=100)
    col1, col2 = st.columns(2)
    with col1:
        people = st.selectbox("На сколько человек?", ["1", "2", "4", "6"])
    with col2:
        format_choice = st.selectbox("Формат ответа", ["Список продуктов", "Список + шаги"])
    submitted = st.form_submit_button("Сгенерировать список покупок")

if submitted:
    with st.spinner("Генерируем..."):
        result = generate_shopping_list(dish, people, format_choice)

    error_markers = ("Напишите", "Слишком длинный", "Не настроен доступ", "Сервис временно", "Не удалось получить", "Пустой ответ", "Не удалось сгенерировать")
    
    if any(result.startswith(marker) for marker in error_markers):
        st.error(result)
    else:
        st.success("Готово!")
        st.text_area("Список покупок", value=result, height=350)
