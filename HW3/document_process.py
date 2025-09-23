from config import get_es
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedding import local_embedding
import time
import tiktoken
from image_table import extract_images_from_pdf, extract_tables_from_pdf


def process_pdf(es_index, file_path):
    pdf_name = file_path.split('/')[-1].split('.')[0]
    es = get_es()
    loader = PyMuPDFLoader(file_path) #如果报错则使用PyMuPDFLoader处理pdf文件
    pages = loader.load()
    ################# 用Cluster生成文件摘要 ################
    # try:
    #     file_summary = generate_summary_for_file(subtitle, pages, file_id, None, user_id, base_id)
    # except Exception as e:
    #     pass

    ################# 提取图片和表格 ################
    image_results = extract_images_from_pdf(file_path)
    print(f'提取图片数量: {len(image_results)}')
    for image_result in image_results:
        embeddings = local_embedding([image_result['context_augmented_image']])
        body = {
            'content': image_result['context_augmented_image'],
            'vector': embeddings[0],
            'file_name': pdf_name,
            'page_num': image_result['page_num'],
            'image_index': image_result['image_index'],
            'image_path': image_result['image_path'],
            'image_summary': image_result['image_summary'],
            'page_context': image_result['page_context'],
            'doc_type': 'image',
        }
        es.index(index=es_index, body=body)
    table_results = extract_tables_from_pdf(file_path)
    print(f'提取表格数量: {len(table_results)}')
    for table_result in table_results:
        embeddings = local_embedding([table_result['context_augmented_table']])
        body = {
            'content': table_result['context_augmented_table'],
            'vector': embeddings[0],
            'file_name': pdf_name,
            'page_num': table_result['page_num'],
            'table_index': table_result['table_index'],
            'table_markdown': table_result['table_markdown'],
            'page_context': table_result['page_context'],
            'doc_type': 'table',
        }
        es.index(index=es_index, body=body)
    textsplit = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100, length_function=num_tokens_from_string)
    chunks = textsplit.split_documents(pages)
    batch = []
    for i, chunk in enumerate(chunks): #收集25个chunks为一批送到嵌入模型，增加速度
        batch.append(chunk)
        if len(batch) == 25 or i == len(chunks) - 1: 
            embeddings = local_embedding([b.page_content for b in batch])
            for j, pc in enumerate(batch):
                body = {
                    'content': pc.page_content,
                    'vector': embeddings[j],
                    'file_name': pdf_name,
                    'doc_type': 'text',
                }
                retry = 0
                while retry <= 5:
                    try:
                        # print(body)
                        es.index(index=es_index, body=body) #写入elastic
                        break
                    except Exception as e:
                        print(f'[Elastic Error] {str(e)} retry')
                        retry += 1
                        time.sleep(1)
            batch = []
            
def num_tokens_from_string(string):   
    encoding = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == '__main__':
    #process_pdf('test_index', 'test_pdf/image_extraction_example.pdf')
    process_pdf('test_index', 'test_pdf/table_extraction_example.pdf')
    process_pdf('test_index', 'test_pdf/test_law_document.pdf')