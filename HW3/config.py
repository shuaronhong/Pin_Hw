from elasticsearch import Elasticsearch
import time

class ElasticConfig:
    url='http://localhost:9200'
    
def get_openai_api_key():
    with open('openAI_API_KEY.txt', 'r') as f:
        api_key = f.read().strip()
    return api_key

def get_es():
    while True:
        try:    
            es = Elasticsearch([ElasticConfig.url],api_key="UjYyWFlwa0JnaDdnMzJscnAzOEc6ZkwtRGxJSnNvVE90UVAzWlJWaVhlZw==") 
            return es
        except:
            print('ElasticSearch conn failed, retry')
            time.sleep(3)
            
EMBEDDING_URL="http://test.2brain.cn:9800/v1/emb"
RERANK_URL="http://test.2brain.cn:2260/rerank"
IMAGE_MODEL_URL='http://test.2brain.cn:23333/v1'
