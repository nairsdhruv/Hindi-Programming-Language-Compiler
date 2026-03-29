from google import genai
import os
from dotenv import load_dotenv
import certifi

# SSL FIX
os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


#------------------- PROMPT BUILDER ------------------
def build_prompt(user_prompt: str) -> str:
    return f"""
You are a STRICT deterministic compiler backend.

You MUST generate ONLY valid code in a custom Hindi programming language.

If output is invalid → FIX internally BEFORE responding.

================= LANGUAGE SPEC =================

Allowed keywords ONLY:

maanlo → variable declaration  
barabar → assignment  
ant → statement end  
kaarya → function  
wapis → return  
ank → int  
agar → if  
warna → else  
jab → while  
likho → print  

Operators:
+ - * / < > <= >= ==

================= DATA RULES =================

1. Variables:
   - Must be lowercase English letters only
   - Example: a, count, total
   - NO spaces, NO special characters

2. Values:
   - ONLY integers (e.g., 0, 1, 10, -5)

3. Expressions:
   - Only use variables and integers
   - Example: a + 1, count - 2

4. Conditions:
   - Must be: <var> <operator> <value/var>
   - Example: a < 10

================= GRAMMAR =================

Program := MainFunction

MainFunction :=
kaarya mukhya() -> ank {{
    Statements
    wapis 0 ant
}}

Statements :=
(Declaration | Assignment | Loop | IfElse | Print)*

Declaration :=
maanlo var : ank barabar value ant

Assignment :=
var barabar expression ant

Loop :=
jab condition {{
    Statements
}}

IfElse :=
agar condition {{
    Statements
}} warna {{
    Statements
}}

Print :=
likho("%d\\n", var) ant

================= HARD RULES =================

1. MUST generate COMPLETE program  
2. MUST include opening AND closing braces  
3. MUST include wapis 0 ant  
4. EVERY statement ends with ant  
5. ONLY allowed keywords  
6. NO explanations, NO comments  
7. NO markdown  
8. NO partial output  
9. NO invalid syntax  
10. DO NOT invent new syntax  

================= FALLBACK RULE =================

If the task is unclear or too complex:
→ Generate a SIMPLE valid program related to the task

================= VALIDATION =================

Before output, ensure:
- Braces count matches
- Every statement ends with "ant"
- Only allowed keywords used
- Variables follow naming rules
- No missing parts

If ANY issue → FIX before output

================= TASK =================

Convert this into the language:

{user_prompt}

================= OUTPUT =================

ONLY return VALID COMPLETE CODE.
NO EXTRA TEXT.
"""



# ------------------ GEMINI ------------------
def generate_gemini(prompt: str) -> str:

    response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
            config={
                "temperature": 0.0,
                "max_output_tokens": 100000,
            }
        )

    if not response or not response.text:
        raise Exception("Empty response from Gemini")

    return response.text.strip()


# ------------------ MAIN SWITCH ------------------
def generate_hindi_code(user_prompt: str) -> str:
    prompt = build_prompt(user_prompt)

    # Priority 2: Gemini
    if client:
        try:
            return generate_gemini(prompt)
        except Exception as e:
            print("⚠️ Gemini failed")

    # Fallback
    print("⚠️ All AI models failed. Returning empty code.")
    return ""

