import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
from profile_data import SYSTEM_PROMPT

app = Flask(__name__)
# aimaden.com dahil tüm domainlerden gelecek isteklere izin veriyoruz
CORS(app, resources={r"/*": {"origins": "*"}})

# Gemini Client (Ortam değişkenindeki GEMINI_API_KEY'i otomatik okur)
client = genai.Client()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "active", "service": "Mehmet Magden Portfolio AI Assistant"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=300,
                temperature=0.4  # Gerçek bilgilere sadık kalması için düşük sıcaklık
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print("Gemini API Error:", str(e))
        return jsonify({"error": "Failed to generate response. Please try again later."}), 500

if __name__ == "__main__":
    # Yerel testler için port 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)