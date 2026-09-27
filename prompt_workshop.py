import os
from dotenv import load_dotenv

load_dotenv()   


# --- Mock response function (users without an API key) ---
def mock_response(prompt):
    """Simulates how prompt quality affects response quality."""
    prompt_lower = prompt.lower()

    # Detect if the prompt has framing
    has_role = any(word in prompt_lower for word in ["you are", "act as", "your role"])
    # Detect if the prompt has constraints
    has_constraints = any(word in prompt_lower for word in
        ["under 100", "in 3 sentences", "as a table", "as json", "format", "bullet"])
    # Detect if the prompt has examples
    has_examples = "input:" in prompt_lower or "example:" in prompt_lower

    quality_score = sum([has_role, has_constraints, has_examples])

    if quality_score == 0:
        return ("[MOCK — Vague prompt detected]\\n"
                "Embeddings are a way to represent data as numbers. "
                "They are used in machine learning and NLP. "
                "There are many types of embeddings.\\n"
                "(This generic response demonstrates what happens with vague prompts.)")
    elif quality_score == 1:
        return ("[MOCK — Decent prompt]\\n"
                "Embeddings convert text into numerical vectors that capture semantic "
                "meaning. Think of it like a GPS coordinate for meaning — similar "
                "ideas get similar coordinates. This is how semantic search works: "
                "instead of matching keywords, you compare meaning vectors.\\n"
                "(Better — the prompt gave some direction.)")
    else:
        return ("[MOCK — Well-engineered prompt]\\n"
                "| Feature | Keyword Search | Semantic Search |\\n"
                "|---------|---------------|-----------------|\\n"
                "| Matching | Exact words | Meaning/intent |\\n"
                "| Handles synonyms | No | Yes |\\n"
                "| Requires | Word overlap | Embedding model |\\n\\n"
                "Think of keyword search like a librarian who only looks at book "
                "titles. Semantic search is a librarian who actually read every book "
                "and can recommend the right one even if you describe it differently.\\n"
                "(Excellent — role + constraints + format produced focused output.)")


def llm_response(prompt):
    """Try real API, fall back to mock."""
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        try: 
            import groq
            client = groq.Groq(
                api_key=api_key,
                timeout=30
            )
            
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Groq API error: {e}")
            return f"API Error: {e}"
    else:
        return mock_response(prompt)



def compare(task_name: str, bad_prompt: str, good_prompt: str):
    """Run both prompts and print results side by side."""
    print(f"\n{'='*60}")
    print(f"TASK: {task_name}")
    print(f"\n--- BAD PROMPT ---\n{bad_prompt}\n")
    print(f"BAD RESPONSE:\n{llm_response(bad_prompt)}")
    print(f"\n--- GOOD PROMPT ---\n{good_prompt}\n")
    print(f"GOOD RESPONSE:\n{llm_response(good_prompt)}")
    
    
    
# ── Task 1 — Code explanation ─────────────────────────────────────────────────
bad_prompt_1 = "Explain st.session_state"

good_prompt_1 = "Your role is a patient, friendly programming instructor who teaches software engineering exclusively to beginners and career changers. Use analogy before technical explanation. Provide a concret example of what Streamlit's st.session_state is and why it is important to understand properly. Give coding example."

compare("Code Explanation — st.session_state", bad_prompt_1, good_prompt_1)


# ── Task 2 — Data formatting ──────────────────────────────────────────────────
TASK_LIST = """
finish the module 7 exercises

review chunking strategies notes

watch the ChromaDB guided example video

start the module project
"""

bad_prompt_2 = (f"convert {TASK_LIST} to JSON output")

good_prompt_2 = (
    f"""Convert {TASK_LIST} to JSON output in the following format:

[
    {{
        "title": "finish module 7 exercises",
        "priority": "medium",
        "status": "pending"
    }}
]

Only return valid JSON output for the four tasks. No prose."""
)

compare("Data Formatting — task list to JSON", bad_prompt_2, good_prompt_2)


# ── Task 3 — System prompt design ────────────────────────────────────────────
bad_prompt_3 = "Be a tutor to help with course questions."

# TODO: Write a good system prompt stored in STUDY_ASSISTANT_SYSTEM_PROMPT below,
#       then write a good_prompt that includes sample context and a question
STUDY_ASSISTANT_SYSTEM_PROMPT = """

    Your role is a study assistant that will help me study course content from
    a provided set of context. If the answer to any question is not founs inside the provided context, you must always answer honestly, stsating that you do not know. Answer only from the provded context. There can be no answers created out of the context of provided. All answers need to be under 150 words in lengt. All answers must include the citation from the document or documents referenced to create the factual response found in the context provided.
"""

good_prompt_3 = "Use the instructions in the system prompt to help me prepare for an uocoming certifcation exam. I want you to communicate in an instructive tone that is also firm in areas where my responses need to be tightended up with more precise technical language. You understand that I am a career changer with six months of experience and must find the best way to patiently provide a learning environment scenario where I am forced to take a step into and up to the next level of my professional development. I need consistent quizzinf to reinforced topics learned, and I need coding exercises from recall to bolster confidence."

compare("System Prompt Design — Study Assistant", bad_prompt_3, good_prompt_3)

# Print the final system prompt
print(f"\n{'='*60}")
print("STUDY ASSISTANT SYSTEM PROMPT:")
print(STUDY_ASSISTANT_SYSTEM_PROMPT)