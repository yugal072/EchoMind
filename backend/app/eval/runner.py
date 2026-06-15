from app.RAG.index import ask, get_retriever
import json

with open("app/eval/dataset.json", "r") as file:
    data = json.load(file)


retriever = get_retriever()

results=[]

for item in data:
    question  = item['question']
    print(f"Running: {question}")
    
    ground_truth = item['answer']
    response = ask(question=question)
    print("Completed")
    
    generated_answer = response['answer']
    
    
    result_structure = {
        "question": question,
        "ground_truth": ground_truth,
        "answer": generated_answer,
        "contexts": response['context']
    }
    
    results.append(result_structure)
    
with open("app/eval/results/results.json", "w") as file:
    file.write(json.dumps(results, indent=4))