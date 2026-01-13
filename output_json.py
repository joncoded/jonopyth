import os
import json
from openai import OpenAI

client = OpenAI(
  api_key=os.environ.get("GROQ_API_KEY"),
  base_url="https://api.groq.com/openai/v1"
)

def get_json_completion(prompt):
  system_prompt = "You are a digital assistant designed to output JSON for machine readability"
  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[      
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": prompt}
    ],
    response_format={"type": "json_object"}
  )
  return response.choices[0].message.content

prompt = input("Enter your question: ")
print("Generating JSON output...\n")
response = get_json_completion(prompt)
json_response = json.loads(response)
print("==== here it is: ====\n")
print(json_response)
print("\n==== enjoy your day! ====\n")