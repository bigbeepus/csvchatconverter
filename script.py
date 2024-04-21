import json
import csv
import os

def format_chat_log(csv_chat_log):

    formatted_examples = []
    current_example = {
        "messages": []
    }
    current_author = None
    current_message_content = ""
    count = 0

    for row in csv_chat_log:
        date, username, usertag, content, mentions, link = row
        author = "assistant" if username == "brotherape" else "user"
        
        if (count == 0) & (username == "brotherape"):
            continue
        if author != current_author:
            if current_message_content:  
                current_example["messages"].append({
                    "author": current_author,
                    "content": current_message_content
                })
                current_message_content = ""  # Reset for the new author
            current_author = author
            count += 1

        current_message_content += content + ". "  # Combine messages
        
        if count == 6:
            if current_message_content:   
                current_example["messages"].append({
                    "author": current_author,
                    "content": current_message_content
                })
        
            formatted_examples.append(current_example)
            current_example = {
                "messages": []
            }
            
            current_author = None
            current_message_content = ""
            count = 0            
            

    formatted_examples.append(current_example)
    return formatted_examples

# Get the directory where the script is located
script_dir = os.path.dirname(__file__)

# Process each CSV file in the directory
for filename in os.listdir(script_dir):
    if filename.endswith(".csv"):
        csv_filepath = os.path.join(script_dir, filename)
        jsonl_filename = filename.replace(".csv", ".jsonl")

        with open(csv_filepath, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            chat_history = list(reader)

        try:
            formatted_data = format_chat_log(chat_history)
            with open(jsonl_filename, "w") as outfile:
                for example in formatted_data:
                    jsonl_line = json.dumps(example, indent=None)  # Use indentation
                    outfile.write(jsonl_line + "\n")  # Add newline after each line
        except ValueError as e:
            print(f"Error processing {filename}: {e}")