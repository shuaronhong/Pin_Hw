from config import get_es,get_openai_api_key
from openai import OpenAI
from embedding import local_embedding

def process_audio(audio_path):
    client = OpenAI(api_key=get_openai_api_key())
    with open(audio_path, 'rb') as f:
        response = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=f)
    return response.text

def add_audio_to_elasticsearch(audio_path):
    audio_text = process_audio(audio_path)
    es = get_es()
    embeddings = local_embedding([audio_text])
    body = {
        "audio_path": audio_path,
        "content": audio_text,
        "vector": embeddings[0],
        "doc_type": "audio",
    }
    es.index(index="test_index", body=body)

if __name__ == "__main__":
    add_audio_to_elasticsearch("audios/test_jay_chow_1.mp3")