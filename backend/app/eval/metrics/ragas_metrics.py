import os
import json
from datasets import Dataset
from langchain_groq import ChatGroq
from ragas import evaluate
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from ragas.llms import LangchainLLMWrapper

import warnings
warnings.filterwarnings("ignore",category=UserWarning, module="ragas")
warnings.filterwarnings("ignore", category=DeprecationWarning)

RESULT_FILE = Path("app/eval/results/results.json")
REPORT_FILE = Path("app/eval/reports/ragas_reports.json")

# Load Results
# Convert to Evaluation dataset
# Run RAGAS metrics
# Return Scores


    # Load results
def load_results(filepath:Path):
    with open(filepath, "r", encoding = "utf-8") as file:
        data = json.load(file)
    return data

def validate_results(results):
    required_fields = {
        "question",
        "answer",
        "ground_truth",
        "contexts"
    }
    
    for idx, row in enumerate(results):
        missing = required_fields - row.keys()

        if missing:
            raise ValueError(
                f"Row {idx} missing fields: {missing}"
            )

        if not isinstance(row["contexts"], list):
            raise TypeError(
                f"Row {idx}: contexts must be list[str]"
            )
            
    # Convert to Evaluation Dataset
def create_dataset(results):
    dataset_dict = {
        "question": [],
        "answer": [],
        "ground_truth": [],
        "contexts": []
    }
    
    for i, row in enumerate(results):
        try:
            question = str(row.get("question", "")).strip()
            answer = str(row.get("answer", "")).strip()
            ground_truth = str(row.get("ground_truth", "")).strip()
            
            # Clean contexts - ensure it's always list of strings
            raw_contexts = row.get("contexts", [])
            if not isinstance(raw_contexts, list):
                raw_contexts = [raw_contexts]
            
            clean_contexts = []
            for ctx in raw_contexts:
                if ctx is None:
                    continue
                clean_ctx = str(ctx).strip()
                if clean_ctx:  # only add non-empty strings
                    clean_contexts.append(clean_ctx)
            
            # Fallback: if no contexts, add empty list
            if not clean_contexts:
                clean_contexts = [""]  
            
            dataset_dict["question"].append(question)
            dataset_dict["answer"].append(answer)
            dataset_dict["ground_truth"].append(ground_truth)
            dataset_dict["contexts"].append(clean_contexts)
            
        except Exception as e:
            print(f"Warning: Skipping row {i} due to error: {e}")
            continue
    
    print(f"Successfully prepared {len(dataset_dict['question'])} samples for evaluation.")
    return Dataset.from_dict(dataset_dict)

def get_evaluator_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Groq_api_key not found in .env")
    groq_llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,  # temperature to be set to 0 as zero creativity 
        api_key=os.getenv("GROQ_API_KEY"),
        max_retries=2,
    )
    
    return LangchainLLMWrapper(groq_llm)

    # Run RAGAS metrics Evaluation
def run_evaluation(dataset):
    evaluator_llm = get_evaluator_llm()
    
    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
        ],
        llm=evaluator_llm
    )
    return result


def save_report(result):
    scores = result.to_pandas().mean(numeric_only = True).to_dict()
    
    # create report file id doesnt exist
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok = True
    )
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent= 4)
        
    return scores


def main():
    print("Loading results...")
    
    results = load_results(RESULT_FILE)
    
    validate_results(results)
    
    dataset = create_dataset(results)
    
    print(f"Evaluating{len(results)} samples...")
    
    result = run_evaluation(dataset)
    
    scores = save_report(result)
    
    print("...Evaluating reports")
    
    for metric, value in scores.items():
        print(f"{metric}: {value:.4f}")
        
        
        
if __name__ == "__main__":
    main()