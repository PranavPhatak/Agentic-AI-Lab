from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader, WebBaseLoader
from dotenv import load_dotenv
load_dotenv()

loader1 = TextLoader("ai.txt")
docs1 = loader1.load()
print(docs1[0].page_content, "\n\n\n")

loader2 = PyPDFLoader("ai.pdf")
docs2 = loader2.load()
print(docs2[0].page_content, "\n\n\n")

loader3 = CSVLoader("ai.csv")
docs3 = loader3.load()
print(docs3, "\n\n\n")

loader4 = WebBaseLoader(web_path="https://docs.langchain.com/oss/python/langchain/streaming")
docs4 = loader4.load()
print(docs4[0].page_content)
