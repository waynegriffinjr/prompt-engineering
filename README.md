# Prompt Engineering Comparison Demo

A Python demonstration that compares **vague prompts** with **well-engineered prompts** and shows how additional context, constraints, roles, examples, and formatting requirements can affect the quality and consistency of an LLM response.

The project can operate in two modes:

1. **Groq API mode** — uses the Groq API when a valid API key is available.
2. **Mock mode** — provides predetermined responses when no API key is configured.

---

## Purpose

This project demonstrates several fundamental prompt-engineering concepts:

* Providing the model with a clear role
* Adding specific constraints
* Providing examples and desired output formats
* Separating vague instructions from precise instructions
* Structuring data for predictable output
* Designing instructions for a study assistant
* Using a mock response system to demonstrate prompt-quality differences without requiring an API key

The project contains three prompt-engineering exercises.

---

## Exercises

### Task 1 — Code Explanation

Compares:

* A simple request to explain `st.session_state`
* A more detailed prompt that establishes the assistant's role, target audience, teaching approach, and requested coding example

This demonstrates how additional context can make an instructional prompt more specific.

---

### Task 2 — Data Formatting

Converts a task list into JSON.

The improved prompt specifies:

* The required JSON structure
* The expected fields
* The number of tasks
* The required output format
* That no additional prose should be returned

This demonstrates how explicit output requirements can improve structured responses.

---

### Task 3 — System Prompt Design

Creates a study-assistant system prompt intended to:

* Ground answers in provided course context
* Avoid inventing information outside that context
* Acknowledge when an answer is not available
* Keep responses under a specified word limit
* Include citations for factual responses

The exercise also demonstrates the distinction between a **system prompt** and a **user prompt**.

---

## Project Structure

A simple project structure can look like:

```text
prompt-engineering/
│
├── prompt_demo.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requirements

* Python 3.9+
* A Groq API key is optional

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```text
python-dotenv
groq
```

The following modules do not need to be installed because they are part of Python's standard library:

```python
import os
```

---

## Environment Variables

The script uses `python-dotenv` to load environment variables from a `.env` file.

Create a file named:

```text
.env
```

and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

Add it to `.gitignore`:

```text
.env
```

---

## How It Works

The script first loads environment variables:

```python
from dotenv import load_dotenv

load_dotenv()
```

It then checks whether a Groq API key exists:

```python
api_key = os.environ.get("GROQ_API_KEY")
```

### API Key Available

If the key exists, the script creates a Groq client and sends the prompt to the selected model.

### No API Key

If no key exists, the script uses:

```python
mock_response(prompt)
```

The mock function analyzes the prompt for several characteristics:

* Role instructions
* Constraints
* Examples

It assigns a basic quality score:

```python
quality_score = sum([
    has_role,
    has_constraints,
    has_examples
])
```

The score determines which simulated response is returned.

---

## Mock Response Scoring

The mock system is intentionally simple. It is not an actual evaluation of LLM response quality.

### Score: 0

The prompt contains none of the recognized prompt-engineering characteristics.

The script returns a generic response representing a vague prompt.

### Score: 1

The prompt contains one recognized characteristic.

The script returns a more focused response.

### Score: 2+

The prompt contains multiple recognized characteristics.

The script returns a structured response representing a well-engineered prompt.

This is intended as a teaching demonstration rather than a scientific measurement of prompt quality.

---

## Running the Program

From the project directory:

```bash
python prompt_demo.py
```

The program will run each exercise and display:

```text
============================================================
TASK: Code Explanation — st.session_state

--- BAD PROMPT ---
...

BAD RESPONSE:
...

--- GOOD PROMPT ---
...

GOOD RESPONSE:
...
```

The same comparison is performed for all three exercises.

At the end, the script prints the study-assistant system prompt.

---

## Key Concepts Demonstrated

### Role

A prompt can establish who the assistant should act as and who it is helping.

Example:

```text
Your role is a patient, friendly programming instructor...
```

### Constraints

Constraints tell the model how the response should be structured.

Examples:

```text
Under 150 words.
```

```text
Only return valid JSON.
```

```text
No prose.
```

### Examples

Providing an example demonstrates the desired output structure.

For example:

```json
{
    "title": "finish module 7 exercises",
    "priority": "medium",
    "status": "pending"
}
```

### Context

Relevant context helps the model understand what the user is actually asking it to accomplish.

### Output Format

Explicitly defining the expected output format can make responses more predictable, particularly when working with structured data such as JSON.

---

## Important Distinction: System vs. User Prompt

A system prompt and a user prompt serve different purposes.

A **system prompt** establishes persistent instructions for how the assistant should behave.

A **user prompt** provides the current request, question, or task.

Conceptually:

```text
SYSTEM
↓
Defines assistant behavior
↓
USER
↓
Provides the current task
↓
MODEL
↓
RESPONSE
```

When using the Groq API, a system prompt should be passed using:

```python
{
    "role": "system",
    "content": system_prompt
}
```

while the user's request should use:

```python
{
    "role": "user",
    "content": prompt
}
```

This distinction is important when building applications that use LLMs.

---

## Learning Goals

After completing this exercise, you should be able to explain:

* Why vague prompts can produce inconsistent responses
* How roles provide behavioral context
* How constraints control output
* Why examples can improve formatting consistency
* Why explicit output requirements are useful
* The difference between system and user messages
* How an application can provide a fallback when an API key is unavailable
* How environment variables can be used to protect API credentials

---

## Security

Never hard-code your API key directly into Python:

```python
# Do NOT do this
api_key = "your-secret-api-key"
```

Instead, store the key in an environment variable:

```env
GROQ_API_KEY=your_api_key_here
```

and retrieve it in Python:

```python
api_key = os.environ.get("GROQ_API_KEY")
```

Make sure `.env` is included in `.gitignore`.

---

## Technologies

* Python
* Groq API
* `python-dotenv`
* Prompt engineering
* JSON
* Environment variables

---

## Disclaimer

The mock response system is intentionally simplified for educational purposes. Its quality score is based only on whether certain predefined phrases or characteristics are present in a prompt. It should not be interpreted as an objective measurement of prompt quality or LLM performance.

This is written as a learning-project README, so it explains **what the code is teaching**, rather than just documenting how to run it.
