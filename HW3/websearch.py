import requests,json,os

from dotenv import load_dotenv

load_dotenv()
WEB_SEARCH_KEY = os.getenv('WEB_SEARCH_KEY')



def bocha_web_search(web_query):
    key=WEB_SEARCH_KEY
    url = "https://api.bochaai.com/v1/web-search"

    payload = json.dumps({
    "query": web_query,
    "count": 10,
    "summary": True,
    })

    headers = {
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.json())
    web_pages = response.json().get('data', {}).get('webPages', {}).get('value', [])

    top_results = []
    for page in web_pages:

        result = {
            'title': page.get('name'),
            'url': page.get('url'),
            'date': page.get('dateLastCrawled'),
            'source': page.get('siteName'),
            'logo': page.get('siteIcon'),
            'summary': page.get('summary'),
            'snippet': page.get('snippet')
        }
        top_results.append(result)
        
    web_articles_text = '\n\n```\n'.join(
        f"标题：{web.get('title', '无标题')}\n"
        f"日期：{web.get('date', '未知日期')}\n"
        f"内容：{web.get('summary', '')}"
        for web in top_results
    )
    return web_articles_text


def ask_llm(query,websearch=None):
    from openai import OpenAI
    
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key="ced64188-f9b4-4244-b020-23cfda56da35"
    )
    
    response = client.chat.completions.create(
        model="deepseek-v3-250324",
        messages=[
            {"role": "user", "content": f"{query}\n\n参考资料：\n{websearch}" if websearch is not None else query}
        ],
        max_tokens=4000,
        timeout=60
    )
    
    return response.choices[0].message.content

if __name__ == '__main__':
    query = "查理柯克遇刺"
    print(ask_llm(query,bocha_web_search(query)))
    # print(bocha_web_search(query))