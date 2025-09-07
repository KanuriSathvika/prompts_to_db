from models import create_table, add_prompt, get_prompt, update_prompt, list_prompts

if __name__ == "__main__":
    # 1. Create table (only first time)
    create_table()

    # 2. Insert new prompts
    add_prompt("Admin", "Chat", "Query", "System_prompt", "main_prompt", "Summarize the document in 200 words")
    add_prompt("Organisation", "Chat", "Generate_questions", "System_prompt", "do", "Generate 10 interview-style questions")

    # 3. Fetch specific prompt
    print("Latest Admin-Chat-Query-System_prompt-main_prompt:")
    print(get_prompt("Admin", "Chat", "Query", "System_prompt", "main_prompt"))

    # 4. Update prompt (creates version 2)
    update_prompt("Admin", "Chat", "Query", "System_prompt", "main_prompt", "Summarize the doc in 150 words with keywords")

    # 5. Fetch again (should show latest)
    print("After update (new version):")
    print(get_prompt("Admin", "Chat", "Query", "System_prompt", "main_prompt"))

    # 6. List all prompts
    print("\nAll stored prompts:")
    for row in list_prompts():
        print(row)
