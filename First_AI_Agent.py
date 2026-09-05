from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def add_numbers(a:int, b:int) -> int:
    """Add two numbers together and return the result.
    Args:
        a (int): The first number to add.
        b (int): The second number to add.
    """
    return a+b

@tool
def multiply_numbers(a:int, b:int) -> int:
    """Multiply two numbers together and return the result.
    Args:
        a (int): The first number to multiply.
        b (int): The second number to multiply.
    """
    return a*b

@tool
def subtract_numbers(a:int, b:int) -> int:
    """Subtract the second number from the first and return the result.
    Args:
        a (int): The first number to subtract.
        b (int): The second number to subtract from the firs.
    """
    return a-b

@tool
def division_numbers(a:int, b:int) -> int:
    """Divide the first number by the second and return the result.
    Args:
        a (int): The first number to divide.
        b (int): The second number to divide by.
    """
    return a/b

model = ChatGroq(model="openai/gpt-oss-120b")

agent = create_agent(
    model = model,
    tools = [add_numbers, multiply_numbers, subtract_numbers, division_numbers],
    system_prompt = "You are a helpful assistant. For maths calculations, you can use the tools provided to you. If you need to add, multiply, subtract or divide numbers, please use the appropriate tool. If you need to perform any other task, please respond with a helpful answer."
)

response = agent.invoke({
    "messages": [
        {
            "role":"user",
            "content": "what is the sum of 5 and 3?"
        }
    ]
})
for res in response["messages"]:
    print(res, "\n")

print(response["messages"][-1].content)