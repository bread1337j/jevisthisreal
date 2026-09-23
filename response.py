from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score
import io
import random


def getWords(filenames: list[str]) -> dict[str, dict[str, None]]:
    """Parses words from a file and returns them as a dictionary (jev formatting req)"""
    out: dict[str, dict[str, None]] = {}
    for filename in filenames:
        wordtype: list[str]
        with open(filename, "r", encoding="utf-8") as f:
            wordtype = f.read().split(',')
        out.update({
                filename.replace(".txt", "").replace("words/", ""):
                {wordtype[x].strip(): None for x in range(0, len(wordtype))}
                })
    print(out.keys())
    return out


async def respondtots(context: str, link: str, words: dict[str, dict[str, None]]) -> str:
    """Creates a response to the message"""
    out: str = ""
    oldToken: str = ""
    token: str = ""
    for i in range(0, 15):
        oldToken = token[:]
        token: str = await append_word(context, out, words)
        print(token)
        if(token == "NONE"):
            return out
        out += " "
        out += token
    return out


async def append_word(context: str, jevString: str, words: dict[str, dict[str, None]]) -> str:
    """having context be a str instead of some builder should be fine
    cause it still has to be shipped off to jev on every iteration
    pylint is making me write poetry"""

    wordtypelist = {x: None for x in words.keys()}
    wordtypelist.update({"NONE": "The sentence is complete. There is nothing to add on. Do not choose this option lightly."})
    TASK = """You are writing a reply one word at a time. Each step you pick only the
        next word. The finished reply should be a grammatical, relevant answer
        to the message, and should end once the thought is complete."""
    

    async with AsyncTypeSafeClient() as client:
        wordtype = await client.system_one(
                state={"task": TASK,
                       "respondingTo": "You are responding to the following string: " + context,
                       "yourResponse": "Your response so far is: " + (jevString.strip() or "(empty: you are choosing the first word)") },
            questions={
                "word": Choice(
                    instructions="What category of word is next in your response? Avoid reusing words unless the grammar requires.",
                    criteria=wordtypelist,
                    )
                }
            )
        category = wordtype.choices["word"].choice
        print(category)
        if(category == "NONE"):
            return "NONE"
        response = await client.system_one(
                state={"task": TASK,
                       "respondingTo": "You are responding to the following string: " + context,
                       "yourResponse": "Your response so far is: " + (jevString.strip() or "(empty: you are choosing the first word)"),
                       "wordType": "The next word must be a: " + category},
            questions={
                "word": Choice(
                    instructions="What is the next word in your response? Avoid reusing words unless the grammar requires.",
                    criteria=words[wordtype.choices["word"].choice],
                    )
                }
        )
    return response.choices["word"].choice

