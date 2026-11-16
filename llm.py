import os
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()

MAX_INPUT_LENGTH = 500
MSG_EMPTY = "Напишите, что хотите приготовить."
MSG_TOO_LONG = "Слишком длинный текст — сократите или разбейте на части."
MSG_AUTH = "Не настроен доступ к сервису."
MSG_SERVER = "Сервис временно недоступен. Попробуйте позже."
MSG_NETWORK = "Не удалось получить ответ. Попробуйте ещё раз."
MSG_EMPTY_RESPONSE = "Пустой ответ модели. Попробуйте переформулировать вопрос."
MSG_UNKNOWN = "Не удалось сгенерировать список. Попробуйте позже."

def generate_shopping_list(dish: str, people: str, format_choice: str) -> str:
    if not dish or not dish.strip():
        return MSG_EMPTY

    if len(dish) > MAX_INPUT_LENGTH:
        return MSG_TOO_LONG

    if format_choice == "Список продуктов":
        format_instruction = "Верни только список продуктов, каждый продукт с новой строки, без лишнего текста."
    else:
        format_instruction = "Верни список продуктов (каждый с новой строки), затем короткие шаги приготовления (5–8 пунктов)."

    prompt = (
        f"Ты помощник по кулинарии. Составь список покупок для блюда: '{dish}'. "
        f"Количество человек: {people}. {format_instruction} Пиши по-русски, без вступлений."
    )

    try:
        giga = GigaChat(
            credentials=os.environ.get("GIGACHAT_CREDENTIALS"),
            model="GigaChat-2",
            verify_ssl_certs=False,
        )
        response = giga.chat(Chat(messages=[Messages(role=MessagesRole.USER, content=prompt)]))
        result_text = response.choices[0].message.content

        if not result_text or not result_text.strip():
            return MSG_EMPTY_RESPONSE

        return result_text.strip()

    except Exception as exc:
        print("DEBUG ОШИБКА:", exc)
        error_text = str(exc).lower()
        if any(code in error_text for code in ("401", "403", "unauthorized", "forbidden")):
            return MSG_AUTH
        if any(code in error_text for code in ("500", "502", "503", "504")):
            return MSG_SERVER
        if any(word in error_text for word in ("timeout", "network", "connection")):
            return MSG_NETWORK
        return MSG_UNKNOWN
