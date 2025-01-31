from openai import OpenAI
from tools.vdb import search_context
import json

client = OpenAI(
    api_key="sk-KQvzzbKNqChegfWRcIrdwcr4SnM8s95Z",
    base_url="https://api.proxyapi.ru/openai/v1",
)

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

def llm_request( messages):
    return client.chat.completions.create(model="gpt-3.5-turbo", messages=messages).choices[0].message.content
            

class Main_agent:
    def __init__(self, storage):
         self.vectors_storage = storage

    def check_is_question_valid(self, question):
         return llm_request(get_check_is_valid_messages(question))

    def get_answer(self, question, context):
         return llm_request(get_fetch_question_messages(question, context))
    
    def process_request(self, question):
        is_question_valid = self.check_is_question_valid(question)
        
        results = search_context(self.storage, question)

        contexts = []
        sources = []

        for document in results:
            contexts.append( document[0].page_content)
            sources.append( document[0].metadata["source"])

        answer = self.get_answer(question, "|".join(contexts))

        if answer: 
            json_answer = json.loads(answer)
            json_answer["sources"] = sources
            return json_answer

        


