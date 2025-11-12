from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(

  model="openai/gpt-4o",
  messages=[
    {
      "role": "user",
      "content": "hi"
    }
  ]
)

print(completion.choices[0].message.content)
