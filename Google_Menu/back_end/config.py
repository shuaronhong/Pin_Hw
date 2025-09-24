def get_openai_api_key():
    with open('back_end/openAI_API_KEY.txt', 'r') as f:
        api_key = f.read().strip()
    return api_key