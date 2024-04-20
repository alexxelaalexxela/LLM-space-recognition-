from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-turbo",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s in this image?"},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://dl.dropboxusercontent.com/scl/fi/a6527edtnuzica6ymnge0/maze1.png",
          },
        },
      ],
    }
  ],
  max_tokens=100,
)

print(response.choices[0])