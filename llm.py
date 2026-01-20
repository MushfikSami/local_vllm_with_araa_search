# ARAA-SEARCH CONFIG (change only this)
ARAA_SEARCH_URL = "http://localhost:8090"  # Your Araa-Search URL
VLLM_URL = "http://127.0.0.1:5000/v1"
VLLM_API_KEY = "no-key"
VLLM_MODEL_NAME = "cpatonn/Qwen3-30B-A3B-Thinking-2507-AWQ-4bit"

# AUTO-DETECT VLLM MODEL
def get_vllm_model():
    from openai import OpenAI
    client = OpenAI(base_url=VLLM_URL, api_key=VLLM_API_KEY)
    models = client.models.list()
    return models.data[0].id if models.data else VLLM_MODEL_NAME

VLLM_MODEL = get_vllm_model()
