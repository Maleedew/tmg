from flask import Flask, render_template_string, request
from huggingface_hub import InferenceClient
from io import BytesIO
import base64
from PIL import Image

app = Flask(__name__)

# Hugging Face API Client Initialization
client = InferenceClient(model="ZB-Tech/Text-to-Image", token="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")

@app.route("/", methods=["GET", "POST"])
def home():
    generated_image = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            # Generate image from prompt
            image = client.text_to_image(prompt)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            generated_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    # HTML and CSS Code (Inline)
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>MD Tech - Text to Image Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 50px;
                background-color: #f4f4f9;
            }
            h1 {
                color: #4A90E2;
            }
            form {
                margin: 20px;
            }
            input[type="text"] {
                width: 60%;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            input[type="submit"] {
                padding: 10px 20px;
                font-size: 16px;
                color: white;
                background-color: #4A90E2;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #357ABD;
            }
            img {
                margin-top: 20px;
                max-width: 80%;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <h1>MD Tech - Text to Image Generator</h1>
        <form method="post">
            <input type="text" name="prompt" placeholder="Enter your text prompt" required />
            <input type="submit" value="Generate Image" />
        </form>
        {% if generated_image %}
        <img src="data:image/png;base64,{{ generated_image }}" alt="Generated Image" />
        {% endif %}
    </body>
    </html>
    """, generated_image=generated_image)

if __name__ == "__main__":
    app.run(debug=True)