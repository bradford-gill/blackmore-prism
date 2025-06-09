import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

response = client.messages.create(
    model="claude-3-5-sonnet-20240620",
    messages=[{"role": "user", "content": "Hello, world! - my name is Andrew"}],
)

print(response.content[0].text)