# jonopyth

an ongoing and growing gathering of python stuff (mostly for wrestling with those enigmatic LLMs!)

## setup

```
git clone https://github.com/joncoded/jonopyth.git
```

### api key

you will require a _free_ [Groq](https://console.groq.com/keys) API key

(_Groq_ is not to be confused with xAI's _Grok_)

#### using the API key on Terminal (Mac/Linux)

```
% export GROQ_API_KEY=your_api_key
```

#### using the API key on Command Prompt (Windows)

```
C:\> set GROQ_API_KEY=your_api_key
```

## demo

after cloning the repo onto your local machine, run this command

on Terminal (Mac/Linux):

```
% python3 anypyfile.py
```

on Command Prompt (Windows): 

```
C:\> python anypyfile.py

## components

* `evalrouting_code_generator.py` (with evaluative routing, make the LLM write code snippets for you!)
* `orchestrated_trip.py` (LLM orchestration travel itinerary maker)
* `output_json.py` (get your prompt as a JSON object)
* `prompt_chaining_summarizer.py` (LLM response summarizer)