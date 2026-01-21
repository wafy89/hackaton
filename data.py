import wikipedia
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

from color_format import COLOR_FORMAT_MAP
from default_text import CONST_PROMPT_TEXT

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


def fetch_wikipedia_article(query):
    return wikipedia.page(title=query, auto_suggest=False,preload=True).content
# def fetch_wikipedia_article(query):
#     # Wikipedia requires a User-Agent (Name + Email/URL)
#     # This prevents your IP from being flagged as a bot.
#     wiki_wiki = wikipediaapi.Wikipedia(
#         user_agent="Hackathon/1.0 (hackathon@gmail.com)",
#         language='en',
#         extract_format=wikipediaapi.ExtractFormat.WIKI
#     )
#
#     page = wiki_wiki.page(query)
#     return page.text


def get_ai_response(questions_count,article_title):
    total_sets = questions_count
    if not OPEN_AI_KEY:
        raise RuntimeError("OpenAI API key is required.")
    wiki= fetch_wikipedia_article(article_title)
    ai = OpenAI(
        api_key=OPEN_AI_KEY,
    )

    while len(wiki) == 0:
        print("No wiki article found. Try again in a few minutes.")
        wiki = fetch_wikipedia_article(article_title)

    response = ai.responses.create(
        model="gpt-5-nano",
        reasoning={"effort": "low"},
        input=(
            f"Analyze the following Wikipedia article: {fetch_wikipedia_article(article_title)}\n\n"
            f"Task: Generate exactly {total_sets} JSON objects.\n"
            f"{CONST_PROMPT_TEXT}"
        ),

    #     input=f"Give me {fact_num} facts about the following article from Wikipedia: {fetch_wikipedia_article(article_title)} "
    #           f"and add another {questions_count} more fake fact that is too close to reality and make it as short as possible to be suitable to be used in quiz app, "
    #           f"and give me the result as a list of python dictionaries and where each dictionary has 3 fact and one fake, where the key is the fact, stated in no longer than 100 characters, "
    #           f"and the value is boolean value and give me only the result in JSON format.",
    )
    raw_output = response.output_text
    try:
        quiz_data = json.loads(raw_output)
        return quiz_data

    except json.JSONDecodeError as e:
        print(f"Failed to parse! Error: {e}")
        print("This is what the AI actually sent:")
        print(raw_output)

def game_logic(questions_count, topic,username):
    final_score = 0
    facts = get_ai_response(questions_count,topic)

    print(f"\nWhich of these is not a fact about {topic}? ")

    for fact in facts:
        index = 0
        print()
        temp = []
        for question, answer in fact.items():
            index += 1
            print(f"{index}-{question}")
            temp.append(f"{index}-{question}")
        user_input = input("\nPlease choose an option between 1 and 4: ")

        while user_input not in  ["1","2","3","4"]:
            user_input = input("\nInvalid input. Please choose an option between 1 and 4: ")

        for value in temp:
            if user_input in value:
                if fact[value[2:]] is False:
                    final_score += 1
                    print(COLOR_FORMAT_MAP["ocean_theme"][0]+f"Well done {username} you go it correctly!"+COLOR_FORMAT_MAP["ocean_theme"][1])
                    break
                else:
                    print(f"Sorry {username} you got it wrong unfortunately!")
                    break
    print(f"\nThank you for playing our game {username}, your final score is { round(( final_score * 100 ) / questions_count )}%.")
