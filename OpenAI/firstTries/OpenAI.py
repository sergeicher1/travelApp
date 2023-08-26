import openai

openai.api_key = "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"

response = openai.Completion.create(
    engine="davinci",  # Choose the engine you want to use
    prompt="Once upon a time",
    max_tokens=50
)

generated_text = response.choices[0].text
print(generated_text)
