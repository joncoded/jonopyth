# jonopyth

an ongoing and growing gathering of python stuff (mostly for wrestling with those enigmatic LLMs!)

## components

* `evalrouting_code_generator.py` 
  * make the LLM write code snippets for you
  * makes use of _evaluative routing_ (iterative improvement)
* `orchestrated_trip.py` 
  * travel itinerary maker
  * makes use of _LLM orchestration_ (splits big task into subtasks)
* `output_json.py` 
  * prompt response as a JSON object
  * makes use of `response_format`
* `prompt_chaining_summarizer.py`
  * LLM response summarizer (get output in 1 sentence and 3 bullet points!)
  * makes use of _prompt chaining_

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
```

note: everything is text-based (no website or local web app yet!)
