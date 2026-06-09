from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Get API key from environment variable (set on Render)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/recipes', methods=['POST'])
def recipes():
    data = request.get_json()
    ingredients = data.get('ingredients', '')
    
    prompt = f"""You are a no-waste chef. User has: {ingredients}. 
    Return 3 realistic recipes using ONLY these plus salt, oil, water, pepper. 
    No fancy extras. If combo is bad, suggest ONE cheap missing ingredient.
    Format each recipe like this:

    1. **Recipe Name**
       - Ingredients (list with dashes)
       - Steps (short, clear)

    2. **Next Recipe**
       ... and so on.

    Use markdown for readability."""
    
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    reply = completion.choices[0].message.content
    return jsonify({"recipes": reply})

if __name__ == '__main__':
    app.run(port=10000)
