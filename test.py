from google import genai

client = genai.Client(api_key="")

res = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Say hello"
)

print(res.text)
