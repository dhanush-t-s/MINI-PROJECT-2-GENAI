from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

# ✅ API key from environment (Render will provide this)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not set")

# ✅ Initialize client (auto reads env variable)
client = genai.Client()

@app.route("/")
def home():
    return {"message": "Gemini 3 API running 🚀"}

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # 🔥 Better prompt engineering
        final_prompt = f"""
        You are a personal growth mentor.

        User question:
        {user_prompt}

        Give:
        - 3 clear actionable steps
        - concise answer
        - practical advice
        """

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=final_prompt
        )

        return jsonify({
            "success": True,
            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)            "response": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
