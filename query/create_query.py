from prompts.prompt_generator import PromptGenerator
from models.llm_model import llm
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from database.db_connection import DatabaseConnection

class CreatQuery :
    def __init__(self,db_connection: DatabaseConnection):
        self.db_connection = db_connection

    def clean_sql_output(self, response):
        return " ".join(response.replace("```sql", "").replace("```", "").replace('\n', " ").strip().split())
    
    def get_schema(self):
        
        return self.db_connection.get_schema()
    
    def query_chain(self):
        
        def get_schemas(_):
            return self.get_schema() 
        prompt = PromptGenerator.generate_sql_prompt()
        return (
            RunnablePassthrough.assign(schema=get_schemas)
            | prompt
            | llm
            | StrOutputParser()
            |(lambda x: self.clean_sql_output(x))

        )





