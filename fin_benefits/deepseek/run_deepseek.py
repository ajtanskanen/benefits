import ollama

model = "deepseek-r1:7b"

while True:
    prompt = input("You: ")
    answer = ollama.generate(model=model, prompt=prompt)
    print("DeepSeek:", answer["response"])