from openai import OpenAI
from openai.types import FileObject
from openai.types.chat import ChatCompletionToolParam,ChatCompletionToolChoiceOptionParam,ChatCompletionMessageParam
import base64 
from typing import List,Iterable
import json
import sys
# sys.path.append('..')
from .config import settings

class IncidentType:
    status:str
    type:str
    def __init__(self, status:str, type: str) -> None:
        self.type = type
        self.status = status

class LLM():
    def __init__(self, api_key: str=settings.OPENAI_API_KEY,base_url:str=settings.OPENAI_BASE_URL,model:str=settings.LLM_MODEL) -> None:
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.messages: List[Iterable[dict]] = []
        self.model = model
    def upload_file(self, file: str):
        response:FileObject = self.client.files.create(
            file=open("/Users/markyangkp/Desktop/Projects/fastapi/app/uploads/5580e90d-cfc7-48e1-a904-9419a586411b.jpg", "rb"),
            purpose='vision'
        )
        file_id = response.id
        return file_id

    def setPrompt(self, prompt: str):
        message = {"role": "system", "content": prompt}
        self.messages.append(message)
        
    def addHistory_User(self, content: str):
        message = {"role": "user", "content": content}
        self.messages.append(message)

    def addHistory_Assistant(self, content: str):
        message = {"role": "assistant", "content": content}
        self.messages.append(message)

    def intelligentsJudgment(self, file_path: str)->IncidentType:
        imageBase64 = "data:image/jpeg;base64," + base64.b64encode(open(file_path, "rb").read()).decode()

        content=[
            {
                "type": "text",
                "text": """
                请判断这张图片属于什么类型的安全事故。需要具体的类型，如爆炸事故、火灾事故等。

                - 如果无法判断，回复“无法判断”
                - 如果可以判断，回复具体的事故类型

                请按照以下格式回复：
                {
                    "status": "# 可以判断：1，不可以判断：-1",  
                    "type": "# 可以判断：具体的事故类型，不可以判断：'无法判断'"  
                }
                """

            },
            {
                "type": "image_url",
                "image_url": {
                "url" : imageBase64
                }
            }
        ]
        self.addHistory_User(content)
        response = self.client.chat.completions.create(
            model=self.model ,
            messages=self.messages
        )
        message_content = response.choices[0].message.content
        self.addHistory_Assistant(message_content)
        # print(message_content)
        jsonddata = json.loads(message_content)

        return IncidentType(jsonddata["status"], jsonddata["type"])

if __name__ == "__main__":
    # url = "https://api.openai.com/v1/"
    # openai1 = OpenAILLM(api_key=api_key,base_url=url)
    # openai1.setPrompt("你是一个聊天助手")
    # print(openai1.ChatToBot("你是谁？"))
    url = "http://10.116.123.30:9997/v1"
    openai1 = LLM(base_url=url,model="glm-4v")
    # print(openai1.upload_file("123"))
    openai1.setPrompt("你是一个负责判断矿山安全事故类型的智能助手")
    # while True:
        # s = input("Mark:")
        # base64处理图片

    data = openai1.intelligentsJudgment("/Users/markyangkp/Desktop/Projects/fastapi/app/uploads/5580e90d-cfc7-48e1-a904-9419a586411b.jpg")
    
    print(data.type)
    