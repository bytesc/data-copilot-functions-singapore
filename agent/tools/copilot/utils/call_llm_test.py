from utils.get_config import config_data

from datetime import datetime
import os

log_path = "./agent_log.txt"

def call_llm(question, llm):
    response = llm.chat.completions.create(
        model=config_data["model_name"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question},
        ],
        stream=False
    )

    answer = response.choices[0].message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}]*********************************************************************" \
                f"\nQ:***\n {question}" \
                f"\nA:***\n {answer.content}\n\n\n\n"

    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(f"Error writing to log file: {e}")

    return answer
