from src.llm.llm import get_llm

llm = get_llm()

response = llm.invoke("Preséntate en una sola frase.")

print(response.content)