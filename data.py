import wikipedia
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


def fetch_wikipedia_article(query):
    print(type(wikipedia.page(query, auto_suggest=False).content))
    return wikipedia.page(query, auto_suggest=False).content


def get_ai_response(questions_count,article_title):
    ai = OpenAI(
        api_key=OPEN_AI_KEY,
    )
    response = ai.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        input=f"Give me {questions_count * 3} facts about the following article from Wikipedia: {fetch_wikipedia_article(article_title)} "
              f"and add another {questions_count} more fake fact that is too close to reality and make it as short as possible to be suitable to be used in quiz app, "
              f"and give me the result as a list of python dictionaries where each dictionary has 3 fact and one fake, where the key is the fact, stated in no longer than 100 characters, "
              f"and the value is boolean value and give me only the result in JSON format.",
    )

    raw_output = response.output_text
    try:
        quiz_data = json.loads(raw_output)
        return quiz_data

    except json.JSONDecodeError as e:
        print(f"Failed to parse! Error: {e}")
        print("This is what the AI actually sent:")
        print(raw_output)

def game_logic():
    final_score = 0
    facts = get_ai_response(10,"Basketball")

    print("Welcome to our game")
    print("Which of these is not a fact about Basketball?")

    for fact in facts:
        index = 0
        print()
        temp = []
        for question, answer in fact.items():
            index += 1
            print(f"{index}-{question}")
            temp.append(f"{index}-{question}")
        user_input = input("\nPlease choose the correct answer:")
        while int(user_input) <= 0 or int(user_input) > 4:
            user_input = input("\nSorry Please choose the correct answer:")
        for value in temp:
            if user_input in value:
                if fact[value[2:]] is False:
                    final_score += 1
                    break
    print(f"\nThank you for using our game your final score is {final_score} out of {len(facts)}")


def main():
    if not OPEN_AI_KEY:
        raise RuntimeError("OpenAI API key is required.")
    game_logic()

if __name__ == "__main__":
    main()
