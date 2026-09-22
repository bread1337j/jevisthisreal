from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score
import io
import random
async def analyzets(context: str, link: str) -> str:
    """analyzes ts"""
    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
                state={"message": context },
            questions={
                "realness": Noul(instructions="Is this real"),
                "tone": Choice(
                    instructions="What is the individual's tone?",
                    criteria={"Calm": None, "Frustrated": None, "Angry": None,
                              "Suspicious": None, "Tomfoolerous": None, "Wise": None,
                              "Unwise": None, "Confused": None, "Thoughtful": None,
                              "Amazed": None, "Wonder": None, "Disappointed": None,
                              "Scared": None},
                ),
                "urgency": Score(
                    instructions="How urgent is this message?",
                    criteria=["Not at all", "Extremely"]
                ),
                "Coherence": Choice(
                    instructions="How coherent is this message?",
                    criteria={"Incomprehensible":None, "Hard to understand":None,
                              "Somewhat understandable":None, "Coherent":None},
               ),
                "pdoom": Score(
                    instructions="What is the probability of doom displayed by this message?",
                    criteria=["0%", "100%"]
                    ),
            },
        )

    builder = io.StringIO()
    builder.write("[Original message]")
    builder.write("(")
    builder.write(link)
    builder.write(")\nDetected realness: ")
    builder.write(f'{int((response.nouls["realness"].noul) * 100)}%')
    builder.write("\nTone: ")
    builder.write(str(response.choices["tone"].choice))
    builder.write("\nUrgency: ")
    builder.write(str(response.scores["urgency"].score))
    builder.write("\nCoherency: ")
    builder.write(str(response.choices["Coherence"].choice))
    builder.write("\np(doom): ")
    builder.write(str(response.scores["pdoom"].score))


    builder.write("\nJev Quotient: ")
    jevquotient = (response.nouls["realness"].noul * 100)
    jevquotient /= (response.scores["urgency"].score * 5 + 1)
    jevquotient *= response.scores["pdoom"].score
    jevquotient += random.random() * 0.1
    builder.write(f"{jevquotient:.5f}")

    result = builder.getvalue()
    builder.close()
    return result
