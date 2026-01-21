import wikipedia
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


def fetch_wikipedia_article(query):
    return wikipedia.page(query, auto_suggest=False).content


def get_ai_response(questions_count,article_title):
    total_sets = questions_count
    if not OPEN_AI_KEY:
        raise RuntimeError("OpenAI API key is required.")

    ai = OpenAI(
        api_key=OPEN_AI_KEY,
    )
    response = ai.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        input=(
            f"Analyze the following Wikipedia article: {fetch_wikipedia_article(article_title)}\n\n"
            f"Task: Generate exactly {total_sets} JSON objects.\n"
            f"Each object must contain exactly 4 entries:\n"
            f"- 3 real facts from the article (max 100 chars each).\n"
            f"- 1 fake fact that sounds highly plausible (max 100 chars each).\n\n"
            f"Format: Return a list of dictionaries where the key is the string statement "
            f"and the value is a boolean (true for real, false for fake).\n"
            f"Constraint: Provide ONLY the JSON array. No conversational text."
        ),

    #     input=f"Give me {fact_num} facts about the following article from Wikipedia: {fetch_wikipedia_article(article_title)} "
    #           f"and add another {questions_count} more fake fact that is too close to reality and make it as short as possible to be suitable to be used in quiz app, "
    #           f"and give me the result as a list of python dictionaries and where each dictionary has 3 fact and one fake, where the key is the fact, stated in no longer than 100 characters, "
    #           f"and the value is boolean value and give me only the result in JSON format.",
    )
    # input = (
    #     f"Analyze the following Wikipedia article: {fetch_wikipedia_article(article_title)}\n\n"
    #     f"Task: Generate exactly {total_sets} JSON objects.\n"
    #     f"Each object must contain exactly 4 entries:\n"
    #     f"- 3 real facts from the article (max 100 chars each).\n"
    #     f"- 1 fake fact that sounds highly plausible (max 100 chars each).\n\n"
    #     f"Format: Return a list of dictionaries where the key is the string statement "
    #     f"and the value is a boolean (true for real, false for fake).\n"
    #     f"Constraint: Provide ONLY the JSON array. No conversational text."
    # ),
    raw_output = response.output_text
    try:
        quiz_data = json.loads(raw_output)
        return quiz_data

    except json.JSONDecodeError as e:
        print(f"Failed to parse! Error: {e}")
        print("This is what the AI actually sent:")
        print(raw_output)

def game_logic(questions_count, topic):
    final_score = 0
    facts = get_ai_response(questions_count,topic)

    print(f"questions_count {questions_count}? ")

    print(f"Which of these is not a fact about {topic}? ")

    for fact in facts:
        index = 0
        print()
        temp = []
        for question, answer in fact.items():
            index += 1
            print(f"{index}-{question}")
            temp.append(f"{index}-{question}")
        user_input = input("\nPlease choose the correct answer: ")

        while user_input not in  ["1","2","3","4"]:
            user_input = input("\nSorry Please choose the correct answer: ")

        for value in temp:
            if user_input in value:
                if fact[value[2:]] is False:
                    final_score += 1
                    print("Well done")
                    break
                else:
                    print("Sorry you got it wrong")
                    break
    print(f"\nThank you for using our game your final score is { round(( final_score * 100 ) / questions_count )}% .")
