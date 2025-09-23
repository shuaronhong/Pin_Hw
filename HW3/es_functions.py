from config import get_es

def create_elasticsearch_index(index_name):
    es=get_es()
    mappings = {
        "properties": {
            "content": {
                "type": "text"
            },
            "vector": {
                "type": "dense_vector",
                "dims": 1024,
                "index": True,
                "similarity": "cosine"
            },
            #metadata
            "file_name": {
                "type": "text"
            },
            "page_num": {
                "type": "integer"
            },
            "chapter": {
                "type": "text"
            },
            "doc_type": {
                "type": "text"
            },
            "language": {
                "type": "text"
            },
            "table_index": {
                "type": "integer"
            },
            "table_markdown": {
                "type": "text"
            },
            "image_index": {
                "type": "integer"
            },
            "image_path": {
                "type": "text"
            },
            "image_summary": {
                "type": "text"
            },
            "page_context": {
                "type": "text"
            },"audio_path":{
                "type": "text"
            }
        }
    }
    try:
        if es.indices.exists(index=index_name):
            print(f"Elasticsearch index {index_name} already exists")
            return
        es.indices.create(index=index_name, mappings=mappings)
        print(f"Elasticsearch index {index_name} created successfully")
    except Exception as e:
        print(f"Error creating elasticsearch index: {index_name}", e)

def delete_elasticsearch_index(index_name):
    es=get_es()
    if not es.indices.exists(index=index_name):
        print(f"Elasticsearch index {index_name} does not exist")
        return
    es.indices.delete(index=index_name)
    print(f"Elasticsearch index {index_name} deleted successfully")

def get_elasticsearch_index_mappings(index_name):
    es=get_es()
    if not es.indices.exists(index=index_name):
        print(f"Elasticsearch index {index_name} does not exist")
        return
    return es.indices.get_mapping(index=index_name)

def put_elasticsearch_new_properties(index_name, properties):
    es=get_es()
    if not es.indices.exists(index=index_name):
        print(f"Elasticsearch index {index_name} does not exist")
        return
    
    es.indices.put_mapping(index=index_name, properties=properties)
    print(f"Elasticsearch index {index_name} new properties added successfully")

if __name__ == "__main__":
    #create_elasticsearch_index("test_index")
    #delete_elasticsearch_index("test_index")
    #print(get_elasticsearch_index_mappings("test_index"))
    put_elasticsearch_new_properties("test_index", {"audio_path": {"type": "text"}})    