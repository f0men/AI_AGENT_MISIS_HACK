import streamlit as st
from openai import OpenAI

# Настройка страницы
st.set_page_config(page_title="Ассистент для абитуриентов МИСИС")

st.markdown("""
    <h1 style='color: #FFFFFF; text-align: center; margin-bottom: 24px; 
               font-size: 28px; font-weight: 600; font-family: -apple-system, BlinkMacSystemFont, sans-serif;'>
        Ассистент для поступления в НИТУ МИСИС
    </h1>
""", unsafe_allow_html=True)

# Проверка наличия секретов
if not all(key in st.secrets for key in ['api', 'folder', 'promt']):
    st.error("Не настроены секреты в Streamlit Cloud. Добавьте api, folder и promt в секреты.")
    st.stop()

# Конфигурация из секретов
API_KEY = st.secrets['api']
FOLDER_ID = st.secrets['folder']
PROMT_ID = st.secrets['promt']

# Модель 
model = f"gpt://{FOLDER_ID}/yandexgpt/rc"

# Инициализация клиента
client = OpenAI(
    base_url="https://rest-assistant.api.cloud.yandex.net/v1",
    api_key=API_KEY,
    project=FOLDER_ID
)

# Инициализация истории чата в session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
# Контейнер для истории чата
chat_container = st.container()

# Отображение всей истории чата
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Поле ввода внизу страницы
prompt = st.chat_input("Задайте вопрос о поступлении в МИСИС...")

if prompt:
    # Добавление вопроса пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Обновляем отображение с новым вопросом
    with chat_container:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Отображение ответа ассистента
    with chat_container:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🤔 Думаю...")
            
            try:
                # Создание запроса
                res = client.responses.create(
                    model=model,
                    prompt={'id': PROMT_ID},
                    input=prompt
                )
                
                # Получение ответа
                answer = res.output_text if hasattr(res.output, 'text') else str(res.output_text)
                
                # Замена текста "Думаю..." на ответ
                message_placeholder.markdown(answer)
                
                # Добавление ответа в историю
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                error_message = f"Ошибка: {str(e)}"
                message_placeholder.markdown(error_message)
                
                # Добавление ошибки в историю
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Минималистичные CSS стили
st.markdown("""
<style>
    /* Весь контейнер поля ввода - БЕЛЫЙ с закругленными углами */
    .stChatInput {
        background-color: #FFFFFF !important;
        border: 1px solid #d1d5db !important;
        border-radius: 20px !important;
        padding: 0 !important;
        margin-top: 16px !important;
        box-shadow: none !important;
    }
    
    /* Внутренний контейнер */
    .stChatInput > div {
        border: none !important;
        background: transparent !important;
        display: flex !important;
        align-items: center !important;
        padding: 8px 12px !important;
    }
    
    /* Текстовое поле - СИНИЙ текст */
    .stChatInput textarea {
        border: none !important;
        background-color: transparent !important;
        font-size: 16px !important;
        color: #007AFF !important;  /* СИНИЙ текст как в сообщениях пользователя */
        box-shadow: none !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        padding: 8px !important;
        height: auto !important;
        min-height: 24px !important;
        line-height: 1.5 !important;
        resize: none !important;
        font-weight: 400 !important;
        width: 100% !important;
        margin: 0 !important;
    }
    
    /* СИНИЙ текст при вводе */
    .stChatInput textarea:not(:placeholder-shown) {
        color: #007AFF !important; /* СИНИЙ */
    }
    
    /* Фокус на поле ввода */
    .stChatInput:focus-within {
        border-color: #007AFF !important; /* Синяя рамка при фокусе */
    }
    
    .stChatInput textarea:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Плейсхолдер - серый текст */
    .stChatInput textarea::placeholder {
        color: #6b7280 !important; /* Оригинальный серый цвет */
        opacity: 1 !important;
        font-weight: 400 !important;
    }
    
    /* Кнопка отправки - не трогаем, оставляем как есть */
    .stChatInput button {
        background-color: #007AFF !important;
        border-radius: 8px !important;
        border: none !important;
        width: 40px !important;
        height: 40px !important;
        min-width: 40px !important;
        margin-left: 8px !important;
        color: white !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }
    
    .stChatInput button:hover {
        background-color: #0056CC !important;
    }
    
    .stChatInput button svg {
        width: 20px !important;
        height: 20px !important;
    }
    
    /* Контейнер для текстового поля */
    .stChatInput > div > div:first-child {
        flex: 1 !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Сообщения чата */
    .stChatMessage {
        margin-bottom: 8px !important;
        padding: 0 !important;
    }
    
    [data-testid="stChatMessage"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 80% !important;
        border: none !important;
        background: none !important;
    }
    
    [data-testid="stChatMessage"][data-message-role="user"] {
        margin-left: auto !important;
        margin-right: 0 !important;
    }
    
    [data-testid="stChatMessage"][data-message-role="assistant"] {
        margin-right: auto !important;
        margin-left: 0 !important;
    }
    
    /* Баббл для сообщений пользователя - синий */
    [data-testid="stChatMessage"][data-message-role="user"] [data-testid="stChatMessageContent"] {
        background-color: #007AFF !important;
        color: white !important;
        padding: 12px 16px !important;
        border-radius: 18px 18px 4px 18px !important;
        margin-left: auto !important;
        max-width: fit-content !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Баббл для сообщений ассистента - серый */
    [data-testid="stChatMessage"][data-message-role="assistant"] [data-testid="stChatMessageContent"] {
        background-color: #F2F2F7 !important;
        color: #1D1D1F !important;
        padding: 12px 16px !important;
        border-radius: 18px 18px 18px 4px !important;
        margin-right: auto !important;
        max-width: fit-content !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Основной контейнер */
    .main .block-container {
        padding-top: 24px;
        padding-bottom: 100px;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

