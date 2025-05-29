from langchain_community.chat_models import ChatOpenAI

def init_chat_model():
    return ChatOpenAI(
        model_name="gpt-4o",  # GPT-4o-mini is included in the gpt-4o endpoint
        temperature=0.7,
        max_tokens=1024,
        model_kwargs={"top_p": 0.9}
    )