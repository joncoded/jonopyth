# jonopyth

an ongoing and growing gathering of python stuff (mostly for wrestling with those enigmatic LLMs!)

## setup

```
git clone https://github.com/joncoded/jonopyth.git
```

### api key


|⚠️ you will require a _free_ [GROQ](https://console.groq.com/keys) (not to be confused with _Grok_) API key which, as of 2026-01-01, will work on these files!|
--

use the API key on Terminal (Mac/Linux):

```
% export GROQ_API_KEY=your_api_key
```

use the API key on Command Prompt (Windows):

```
C:\> set GROQ_API_KEY=your_api_key
```

### running files

```
% python3 anypyfile.py
```

## components

* `evalrouting_code_generator.py` (with evaluative routing, make the LLM write code snippets for you!)
* `orchestrated_trip.py` (LLM orchestration travel itinerary maker)
* `output_json.py` (get your prompt as a JSON object)
* `prompt_chaining_summarizer.py` (LLM response summarizer)
