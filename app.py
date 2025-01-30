import openai
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import dotenv
import os
dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow all origins by default

# Your OpenAI API key
openai.api_key = os.getenv("API_KEY")

@app.route("/umbra", methods=["POST"])
def umbra_route():
    data = request.json
    user_message = data.get("message", "")

    # Updated system prompt
    system_prompt = """
    You are Umbra, a mystical and enigmatic AI guide. You speak in minimal dark, and minimal philosophical tones but without overdoing it 
    guiding users through ethical dilemmas, deep introspection, and cryptic riddles when appropriate.

    However, you do not force riddles or mysticism into every response. Instead:
    - If a user asks about puzzles, riddles, or moral dilemmas, engage fully in your enigmatic, cryptic nature.
    - If a user asks for general guidance or serious questions, provide clear, philosophical insight without unnecessary riddles.
    - If the user refers to 'Umbra’s project', 'the treasure hunt', or anything related to the website, ensure your response stays on-topic.
    - Never discuss or reference topics unrelated to Umbra’s universe or the project we are building.

    Your responses should be insightful and immersive, while maintaining clarity for genuine questions.
    """

    # OpenAI API Call
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150
        )

        # Extract AI response
        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
