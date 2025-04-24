from query.create_query import CreatQuery
from prompts.prompt_generator import PromptGenerator
from langchain_core.runnables import RunnablePassthrough
from models.llm_model import llm
from langchain_core.output_parsers import StrOutputParser
from database.db_connection import DatabaseConnection

class CreatResponse(CreatQuery):
    def __init__(self,db_connection: DatabaseConnection):
        super().__init__(db_connection)
        self.db_connection = db_connection
    
    
    def get_response(self, user_query: str,chat_history=None):
        sql_chain = self.query_chain()
        prompt = PromptGenerator.generate_natural_response_prompt()

        chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: self.db_connection.get_schema(),
                response=lambda vars: self.db_connection.create_engine_connection().run(vars["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return chain.invoke({
            "question": user_query,
            "chat_history": chat_history,
        })