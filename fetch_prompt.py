from models import get_prompt

prompt = get_prompt(
    level="Admin",
    feature="Chat",
    section="System_prompt",
    sub_section="main_prompt",
    purpose="Query"
)

if prompt:
    print("✅ Found Prompt:", prompt)
else:
    print("❌ No prompt found for given filters")
