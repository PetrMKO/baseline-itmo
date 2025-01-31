import requests

from openai import OpenAI

client = OpenAI(
    api_key="sk-KQvzzbKNqChegfWRcIrdwcr4SnM8s95Z",
    base_url="https://api.proxyapi.ru/openai/v1",
)

def api_request(body):
        api_url="https://api.proxyapi.ru/openai/v1/chat/completions"
        api_key="sk-KQvzzbKNqChegfWRcIrdwcr4SnM8s95Z"


        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key
        }

        return requests.post(api_url, headers, json = body)

def get_check_is_valid_messages (question):
     return [
       
            {
                "role": "system",
                "content": "Ты помошник отвечающий на тесты. Тебе на вход подается строка - вопрос следующего вида - вопрос потом символ \n потом пронумерованные варианты ответов, разделенные символом \n. Как вопрос, так и варианты ответов могут содержать символ \n внутри. Вопросы, которые тебе задаются, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10. Каждый вариант ответа соответствует определённому утверждению или факту. Ты должен определить содержит ли вопрос варианты ответов и подразумевает ли вопрос выбор вариантов ответа. Если нет, то ты должен вернуть false, если да, то ты должен вернуть true"
            },
            {
                "role": "user",
            
                "content": question
            }
    ]

def get_fetch_question_messages (question, context):
     return [
       
            {
                "role": "system",
                "content": "Ты помошник отвечающий на тесты. Тебе на вход подается строка - вопрос следующего вида - вопрос потом символ \n потом пронумерованные варианты ответов, разделенные символом \n. Как вопрос, так и варианты ответов могут содержать символ \n внутри. Вопросы, которые тебе задаются, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10. Каждый вариант ответа соответствует определённому утверждению или факту. Ты должен определить правильный вариант ответа и вернуть его номер (это очень важно - только номер, без содержания ответа) в поле answer JSON-ответа. Если вопрос не предполагает выбор из вариантов, или вариантов ответа нет:, то поле answer должно содержать null."
            },
              {
                "role": "assistant",
                "content": context
            },
            {
                "role": "user",
            
                "content": question
            }
        ]

class AgentRequest:
    def llm(self, messages):
        return client.chat.completions.create(model="gpt-3.5-turbo", messages=messages).choices[0].message.content
            

class Main_agent:
    def check_is_question_valid(self, question):
         Fetch = AgentRequest()
         return Fetch.llm(get_check_is_valid_messages(question))

    def get_answer(self, question, context):
         Fetch = AgentRequest()
         return Fetch.llm(get_fetch_question_messages(question, context))