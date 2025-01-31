from openai import OpenAI
from tools.vdb import search_context, config_vectors_storage_push
from tools.google_search import get_sources_and_context

import json

client = OpenAI(
    api_key="sk-KQvzzbKNqChegfWRcIrdwcr4SnM8s95Z",
    base_url="https://api.proxyapi.ru/openai/v1",
)

def get_check_is_valid_messages (question):
     return [
       
            {
                "role": "system",
                "content": "Ты помошник отвечающий на тесты. Тебе на вход подается строка - вопрос следующего вида - вопрос потом символ \n потом пронумерованные варианты ответов, разделенные символом \n. Как вопрос, так и варианты ответов могут содержать символ \n внутри. Вопросы, которые тебе задаются, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10. Каждый вариант ответа соответствует определённому утверждению или факту. Ты должен определить содержит ли вопрос варианты ответов и подразумевает ли вопрос выбор вариантов ответа. Если вопрос не подразумевает выбор ответа, то верни false. Если не имеет вариантов ответа, то тоже верни false. Если вопрос подразумевает выбор ответа, а также есть варианты ответа, то ты должен вернуть true"
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
                "content": "Ты помошник отвечающий на тесты. Тебе на вход подается строка - вопрос следующего вида - вопрос потом символ \n потом пронумерованные варианты ответов, разделенные символом \n. Как вопрос, так и варианты ответов могут содержать символ \n внутри. Вопросы, которые тебе задаются, почти всегда содержат варианты ответов, пронумерованные цифрами от 1 до 10. Каждый вариант ответа соответствует определённому утверждению или факту. Ты должен определить правильный вариант ответа и вернуть его номер (это очень важно - только цифра, соответствующая варинату ответа) в поле answer JSON-ответа. Ты не должен никаким образом обофрмлять json, не надо никаких оформлений в виде code-style. Только json. Если вопрос не предполагает выбор из вариантов, или вариантов ответа нет, то поле answer должно содержать null. Также ты должен указать краткое обоснование ответа в поле reasoning. Обоснование должно отталкиваться от контекста. Если вопрос не подразумевает выбор ответа, или вариантов ответа нет, то в поле answer должен быть null, а в поле reasoning должен быть ответ и обоснование."
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
    return client.chat.completions.create(model="gpt-4o-mini", messages=messages).choices[0].message.content
            

class Main_agent:
    def __init__(self, storage, logger):
         self.vectors_storage = storage
         self.logger = logger

    def check_is_question_valid(self, question):
         return llm_request(get_check_is_valid_messages(question))

    def get_answer(self, question, context):
         return llm_request(get_fetch_question_messages(question, context))
    
    async def process_request(self, question):
        is_question_valid = self.check_is_question_valid(question)
        
        await self.logger.info(self.vectors_storage)

        results = search_context(self.vectors_storage, question)

        if len(results):
            contexts = []
            sources = []

            for document in results:
                contexts.append( document[0].page_content)
                sources.append( document[0].metadata["source"])

            answer = self.get_answer(question, "|".join(contexts))

            await self.logger.info(answer)

            if answer: 
                json_answer = json.loads(answer)
                json_answer["sources"] = sources
                return json_answer
        
        [contexts, sources] = await get_sources_and_context(question, self.logger)

        # Тут можно было добиваться ответа, пока не надется нужный контекст,
        # но ограничение по времени на запрос такое сделать не позволит, поэтому попытка только одна

        answer = self.get_answer(question, "|".join(contexts))

        await self.logger.info(f"after req {answer}")


        if answer: 
            json_answer = json.loads(answer)
            json_answer["sources"] = sources

            for i in range(len(contexts)):
                config_vectors_storage_push(self.vectors_storage, contexts[i], sources[i])
            
            return json_answer
        
        return  {
                "answer": None,
                "reasoning": "",
                "sources": []
            }
                    
        


