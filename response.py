from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score
import io
import random


def getWords(filename: str) -> dict[str, None]:
    """Parses words from a file and returns them as a dictionary (jev formatting req)"""
    out: list[str] = []
    with open(filename, "r", encoding="utf-8") as f:
        out = f.read().split('\n')
    return {out[x]: None for x in range(0, len(out))}


async def respondtots(context: str, link: str, words: dict[str, None]) -> str:
    """Creates a response to the message"""
    out: str = ""
    oldToken: str = ""
    token: str = ""
    for i in range(0, 15):
        oldToken = token[:]
        token: str = await append_word(context, out, words)
        #print(token)
        if(token == oldToken or token == "stop"):
            return out
        out += " "
        out += token
    return out


async def append_word(context: str, jevString: str, words: dict[str, None]) -> str:
    """having context be a str instead of some builder should be fine
    cause it still has to be shipped off to jev on every iteration
    pylint is making me write poetry"""
    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
                state={"respondingTo": "You are responding to the following string: " + context,
                       "yourResponse": "Your response so far is: " + jevString },
            questions={
                "word": Choice(
                    instructions="What is the next word in your response? Reply 'stop' if and only if you have nothing else to say. Your reply MUST contain something.",
                    criteria=words,
                    )
                }
        )
    return response.choices["word"].choice

