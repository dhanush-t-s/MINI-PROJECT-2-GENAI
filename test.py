from google import genai

client = genai.Client(api_key="AIzaSyCdin0Tx9MWgFyvlNYuGkNlUDl8rfWwFRI")

res = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Say hello"
)

print(res.text)