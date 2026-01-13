import os
import json
from openai import OpenAI

# connect to the client
client = OpenAI(
  api_key=os.environ.get("GROQ_API_KEY"),
  base_url="https://api.groq.com/openai/v1"
)

system_role = "you are a helpful coding assistant who can introduce short snippet to students of web development"

# chat completion function
def get_completion(prompt, system_prompt=system_role, json_mode=False):
  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
      {"role": "system", "content": system_prompt}, 
      {"role": "user", "content": prompt}],
      response_format={"type": "json_object"} if json_mode else None
  )
  return response.choices[0].message.content

# reusable criteria for snippet evaluation
snippet_criteria = '''
  <criteria>
  please evaluate the following code snippet task: {task} ... and evaluate based on these criteria:
  1. Completeness: is the task vague or well-defined? 
  2. Simplicity: does the task involve a single feature? 
  3. Clarity: will the instructions be clear and easy to follow?
  4. Environment accuracy: are the techniques appropriate for the framework or library or programming language?
  5. Feasibility: can a student of web development follow the snippet easily?
  6. Reusability: can a student use this snippet to build a wide variety of apps with it
  7. Conciseness: does the snippet focus on the core task and is free of unnecessary code? 
  </criteria>
'''

# initial prompt
def get_snippet_evaluation_prompt(snippet, task):
  return f"""You are a professional web developer evaluating code snippet quality for {task}.

  <criteria>
  {snippet_criteria}
  </criteria>
  
  <snippet>
  {snippet}
  </snippet>
  
  <instructions>
  Respond with a JSON object containing:
  1. "decision": Either "good" (meets standards) or "needs_work" (requires revision)
  2. "reason": Brief explanation of your decision
  3. "feedback": Specific suggestions for improvement if needed. 
  (If the question is good, the "feedback" property should be an empty string.)
  </instructions>
  
  <format>
  {{
    "decision": "good or needs_work",
    "reason": "your reasoning here",
    "feedback": "your specific feedback here"
  }}
  </format>

  <output_rules>
  Output ONLY the JSON, nothing else.
  Do not include any markdown backticks in your response.
  </output_rules>
  """

# revision prompt
def get_snippet_revision_prompt(snippet, task, feedback):

  # simply return the improved snippet
  return f"""You are a professional web developer. Use the following feedback to improve the snippet for {task}.
  Return the revised snippet in the same format as the original snippet. Output ONLY the snippet with no other commentary. Ensure that any markdown backticks are closed properly. 
  
  <snippets>
  {snippet}
  </snippets>

  <criteria>
  {snippet_criteria}
  </criteria>

  <feedback>
  {feedback}
  </feedback>
  
  Your improved snippet:"""
    
# evaluative routing 
def route_snippet_request(test_snippet, task, max_tries=3, current_try=1): 
  
  # decision on the snippet
  evaluation_prompt = get_snippet_evaluation_prompt(test_snippet, task)
  evaluation_response = get_completion(evaluation_prompt, json_mode=True)    
  evaluation_data = json.loads(evaluation_response)
  decision = evaluation_data["decision"]  
  print(f"\n======== 📋 evaluation decision: {decision} \n")
  
  # routing by evaluation 
  if decision == "good":    
    
    # if it meets standards then stop
    print("======== ✅ snippet meets quality standards! returning to user...\n")
    print(f"* reason: {evaluation_data['reason']}\n")
    print(f"* snippet: {test_snippet}\n")
    print(f"\n\n enjoy coding! 🎉🎉🎉\n")
    return test_snippet
  
  else:
  
    # if it needs work
    print(f"======== ⚠️ snippet needs work! sending to revision prompt...\n")
    print(f"* reason: {evaluation_data['reason']}\n")
    print(f"* feedback: {evaluation_data['feedback']}\n")
        
    if current_try >= max_tries:
    
      # rate limit to prevent API overuse
      print("\n=== 🛑 === error: maximum number of tries reached!\n")
      return test_snippet
    
    else:            
    
      # revise snippet
      revision_prompt = get_snippet_revision_prompt(test_snippet, task, evaluation_data['feedback'])
      revised_snippet = get_completion(revision_prompt)
      print(f"\n=== ❇️ === revised snippet: \n\n {revised_snippet}\n")

      # recursively evaluate revised snippet
      return route_snippet_request(revised_snippet, task, max_tries, current_try+1)

# ==== RUNTIME

# sample training snippet
test_snippet = """
HTML table
Requirements:
- browser
- text editor
- basic HTML knowledge
Instructions:
1. open your text editor and create a new file named "index.html"
2. add the basic structure at the top of the file:
  ```html
    <!DOCTYPE html>
    <html>
      <head>
        <title>My First Table</title>
      </head>
      <body>    
  ```
3. inside the <body> tags, add the <table> element:
  ```html
      <table border="1">
        <tr>
          <th>Header 1</th>
          <th>Header 2</th>
        </tr>
        <tr>
          <td>Row 1, Cell 1</td>
          <td>Row 1, Cell 2</td>
        </tr>
        <tr>
          <td>Row 2, Cell 1</td>
          <td>Row 2, Cell 2</td>
        </tr>
      </table>
  ```
4. close the <body> and <html> tags:
  ```html
      </body> 
    </html>
  ```
5. save the file and open it in your web browser to see your table
"""

# the request
test_task = input("what do you want to create today? ")
result = route_snippet_request(test_snippet, test_task)