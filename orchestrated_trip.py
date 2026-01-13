import os
import json
from openai import OpenAI

# === CONNECTION TO LLM

client = OpenAI(
  api_key=os.environ.get("GROQ_API_KEY"),
  base_url="https://api.groq.com/openai/v1"
)

# === PRE-PROMPTING (END-USER CONFIGURATION)

def get_integer_input(question):
    while True:
        user_input = input(question)
        try:
            # attempt to convert the input to an integer
            number = int(user_input)
            break  # exit the loop if successful
        except ValueError:
            # handle the error if the conversion fails
            print(f"'{user_input}' is not a valid number; please try again!")
    return number

trip_destination = input("What is the destination? ")
trip_length = get_integer_input("How long is the trip (in days)? ")
trip_budget = get_integer_input("What is your approximate budget in US $? ")
trip_party_adults = get_integer_input("How many adults are going on the trip? ")
trip_party_children = get_integer_input("How many children are going on the trip? ")
trip_season = input("When is the trip taking place? ")
trip_wishes = input("What are the goals of the trip? ") or "no preference"
print("\nPlanning the trip...\n\n")

# === CHAT FUNCTIONS

# chat completion function
def get_completion(prompt, system_prompt="You are a digital assistant", json_mode=False):  
  response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
      {"role": "system", "content": system_prompt}, 
      {"role": "user", "content": prompt}
    ],
    response_format={"type": "json_object"} if json_mode else None
  )
  return response.choices[0].message.content

# prepare a list to store the subtask responses
subtask_solutions = []

# prepare a function to perform a subtask
def execute_subtask(subtask, subtask_prompt):

    # avoiding KeyError
    content = subtask.get('content', '').strip()
    budget = subtask.get('budget', 'Not specified')

    if not content:
        print("Warning: subtask is missing 'content' — proceeding with empty content")

    # build a fresh prompt 
    prompt = subtask_prompt + f"""
    <subtask_content>
    {content}
    </subtask_content>

    <subtask_budget>
    {budget}
    </subtask_budget>
    """

    try:
        result = get_completion(prompt)
    except Exception as e:
        # catch API or other runtime errors to avoid stopping the whole run
        print(f"Error executing subtask: {e}")
        result = f"ERROR: {e}"

    subtask_solutions.append(result)

# put all the subtasks' results together
def fuse_solutions(subtask_solutions, final_prompt): 

    combined_solutions = "\n\n".join(subtask_solutions)

    final_prompt = final_prompt + f"""
    <detailed_plans>
    {combined_solutions}
    </detailed_plans>"""   

    # prompt the LLM to make a final plan
    return get_completion(final_prompt)

# === PROMPT TEMPLATES

# motivation based on user input
prompt_intro = f"""
  Your task is to help plan a {trip_length} day vacation to {trip_destination} 
  during {trip_season} for {trip_party_adults} adults and {trip_party_children} children, 
  who have also these preferences: {trip_wishes}. 

  The budget is ${trip_budget} (US dollars).

  You'll organize a list of subtasks involved in the trip.
  Try to cover everything they will need to make great memories.
"""

# make the initial prompt for the big complex task that specifies aspects of the task in <custom_xml_tags> 
# to developer: don't worry about what to name these tags as the LLM will figure it out

initial_prompt = f"""
  <task>
    
    {prompt_intro}

    Output your result as a JSON object with the key "data" containing a list of 
    subtasks in the format specified below.

    Each "content" field should be a description of everything the travel party 
    will need to figure out to accomplish this subtask on our trip.

    Make the content field about one paragraph long.
  </task>

  <budget>
    ${trip_budget}
  </budget>

  Output ONLY valid JSON below. No markdown backticks.
  """

subtask_prompt = f"""
  <task>
    
    {prompt_intro}

    Output a 2-3 short sentences using your innate knowledge to offer 
    your final recommendation on what to do and purchase.

    Itemize what you'd spend this subsection of the budget on 
    to the best of your knowledge. Begin your output with a 1-3 word description,
    then 2-3 short sentences with an itemized spending plan (if needed).

  </task>
  """

final_prompt = f"""
  <task>

    Your task is to condense a detailed list of plans for an upcoming trip to 
    {trip_destination} into a single, short summary.

    Include only actionable information to carry out the trip.

    Output the following:
    - Offer a detailed, time-based itinerary
    - List out all purchases
    - Specify locations, times, and contingency plans
    - Use bullet point lists

  </task>
  """

# === RUNTIME : AUTOMATED!

# the LLM will take the initial_prompt above and generate a JSON list of subtasks
json_string = get_completion(initial_prompt, json_mode=True)
result = json.loads(json_string)
subtasks = result["data"]

# execute the subtasks with the subtask_prompt template
for subtask in subtasks:
  execute_subtask(subtask, subtask_prompt)

# get the final results of the big task with a final_prompt
final_plan = fuse_solutions(subtask_solutions, final_prompt)
print(final_plan)