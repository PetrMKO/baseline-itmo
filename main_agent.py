import requests
from dotenv import dotenv_values

config = dotenv_values(".env")

def api_request(body):
        api_url=config.LLM_API_URL
        api_key=config.LLM_API_KEY

        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        return requests.post(api_url, headers, json = body)

def get_check_is_valid_messages (answer: str):
     return [
       
            {
                "role": "system",
                "content": "Ты помошник отвечающий на тесты. Тебе на вход подается строка - вопрос следующего вида - вопрос потом символ \n потом пронумерованные варианты ответов, разделенные символом \n. Как вопрос, так и варианты ответов могут содержать символ \n внутри. Вопросы, которые тебе задаются, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10. Каждый вариант ответа соответствует определённому утверждению или факту. Ты должен определить содержит ли вопрос варианты ответов и подразумевает ли вопрос выбор вариантов ответа. Если нет, то ты должен вернуть false, если да, то ты должен вернуть true"
            },
            {
                "role": "user",
            
                "content": str
            }
        ]

class AgentRequest:
    
    def llm(messages):
        return api_request({
            "model": "gpt-4-turbo",
             "messages": messages
            })
            

class Main_actor:

    def check_is_answer_valid(answer: str):
         Fetch = AgentRequest()
         Fetch.llm(str)