from typesafe_sdk import AsyncTypeSafeClient, Choice, Noul, Score
import io
async def analyzets(context: str) -> str:
    """analyzes ts"""
    async with AsyncTypeSafeClient() as client:
        response = await client.system_one(
            state={"message": context},
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
                    criteria=["Can wait", "This week", "Today"],
                ),
            },
        )

    builder = io.StringIO()
    builder.write("Detected realness: ")
    builder.write(str(response.nouls["realness"].noul))
    builder.write("\nTone: ")
    builder.write(str(response.choices["tone"].choice))
    builder.write("\nUrgency: ")
    builder.write(str(response.scores["urgency"].score))
    result = builder.getvalue()
    builder.close()
    return result
