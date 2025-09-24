import openai
from config import get_openai_api_key
import base64
import mimetypes
import json

def extract_menu_items(image_path,to_language):
    client = openai.OpenAI(api_key=get_openai_api_key())
    prompt = f"""
    请提取图片中的所有菜品名称，确保不要遗漏，也不要编造菜谱上不存在的菜品。
    然后需要进行翻译工作，并返回一个字典以json的格式，具体要求如下:
    - 菜品名称原文需要是你从图片中自动提取的语言原文，不需要翻译，只需提取。
    - 菜品名称原文是字典的key，不要翻译，后面跟随的value也是一个字典，规则如下
    - value字典里面有三个key，分别是translated_name，ingredients_and_seasonings,flavor_and_preparation,不要进行任何翻译！必须保持严格固定是这三个key！
    - value字典里面的values的所有文字，都必须以{to_language}翻译。
    - 也就是说只有value字典里面的values是需要翻译成{to_language}的，其他部分都不能进行翻译！
    输出格式如下：
    {{"菜品名称原文1":{{
        "translated_name":"菜品翻译后名称1",
      "ingredients_and_seasonings":[原料1-1，原料1-2，...，作料1-1....]，
      "flavor_and_preparation":"描述菜品的口味答题是怎么样的，做法大概是怎么做出来的"}}，
      "菜品名称原文2":{{
        "translated_name":"菜品翻译后名称2",
      "ingredients_and_seasonings":[原料2-1，原料2-2，...，作料2-1....]，
      "flavor_and_preparation":"描述菜品的口味答题是怎么样的，做法大概是怎么做出来的"}}，
      ...              
    }}
    """
    mime_type = mimetypes.guess_type(image_path)[0] or 'image/png'
    with open(image_path, "rb") as img:
        content_bytes = img.read()
    encoded = base64.b64encode(content_bytes).decode('utf-8')
    response = client.chat.completions.create(
        model="gpt-5-mini",   # or gpt-4o
        messages=[
            {"role": "system", "content": "你是一个小助手，专门提取菜单图片中的菜品名称，并返回一个结构性的json数据"},
            {"role": "user", 
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded}"}},
                {"type": "text", "text": prompt}]
            }
        ],
    )
            
    return response.choices[0].message.content

if __name__ == "__main__":
    result = extract_menu_items("back_end/images/Snipaste_14.png", "英文")
    print(result)
    with open("back_end/menu_json/Snipaste_14.json", "w") as f:
        json.dump(result, f)