from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
Gorq_api = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0,max_tokens=256,api_key=Gorq_api)
