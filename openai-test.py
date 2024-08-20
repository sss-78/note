from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

try:
    completion = client.chat.completions.create(
        model="text-davinci-003",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )
except:
    print('Error: 429')


print(completion.choices[0].message)