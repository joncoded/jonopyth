import os
from openai import OpenAI

client = OpenAI(
  api_key=os.environ.get("GROQ_API_KEY"),
  base_url="https://api.groq.com/openai/v1"
)

def get_completion(prompt):
  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{
      "role": "user",
      "content": prompt
    }],
  )
  return response.choices[0].message.content

def summarize(original_prompt, original_result):
  
  chained_prompt = f'''
    <context>
      Here is the original prompt:
      {original_prompt}
      Below is the original result: 
      {original_result}
    </context>
    <request>
      You are a summarizing agent for busy people. Write a summary of the context with 3 bullet points (no more than 25 words each), each with a direct response to the prompt
    </request>
    <guidelines>
    - Begin the summary that summarizes the prompt
    - Do not try to insert any more information in each bullet point then what the prompt asks, e.g. if the prompt asks for hotels, just list the hotel's name in each bullet point!
    </guidelines>
  '''
  return get_completion(chained_prompt)

def prompt_chain(prompt):
  print("\n\n LLM is thinking...")
  original_result = get_completion(prompt)
  print("\n\n ==== Unabridged version: \n", original_result)
  summary = summarize(prompt, original_result)  
  print("\n\n ==== Summarized version: \n", summary)
  print("\n\n ==== End of summary ==== \n\n")
  
prompt = input("Ask a question: ")
prompt_chain(prompt)