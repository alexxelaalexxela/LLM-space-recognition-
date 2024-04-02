from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "you are in a maze and you have to find the exit, take in count all the previous informations. just answer the number of th room/way you choose"},
        {"role": "user", "content": "you are in a room with door 1 and door 2 where do you go?"},
    ]
)

print(completion.choices[0].message.content)
