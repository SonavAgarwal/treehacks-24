from dotenv import load_dotenv
import os
import openai

load_dotenv()
together_key = os.getenv("TOGETHER_KEY")

client = openai.OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=together_key)


# ===========================
# find_best_filenames(file_names, query)
# ===========================

def find_best_filenames(filenames, query):
    prompt = f"""
        You are looking for files that are most relevant to the given query. For each file, score it from 1 to 10 based on how likely it is to be relevant to the query. The higher the score, the more relevant the file is. If you are not sure, set score to -1.
        For example:
        query: code that uses axios
        files: main.js, api.js, index.js, package.json, README.md
        would be converted to:
        {{
            "main.js": 7,
            "api.js": 9,
            "index.js": 4,
            "package.json": 0,
            "README.md": 0,
        }}
    """

    print(prompt)

    response = client.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        messages=[
            {
                "role": "system",
                "content": prompt
            }, {
                "role": "user",
                "content": f"query: {query}\nfiles: {', '.join(filenames)}"
            }
        ]
    )

    return response
