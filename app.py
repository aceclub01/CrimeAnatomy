import os
from app import app
from flask import Flask, render_template

app = Flask(__name__)

def parse_slides():
    slides = []
    with open('slides.txt', 'r') as file:
        content = file.read().strip().split('\n\n')  # Separate slides by blank line

    for slide_text in content:
        lines = slide_text.split('\n')
        title = lines[0]  # The first line is the title
        body = lines[1:]  # The rest are the body content
        
        slides.append({'title': title, 'content': body})
    
    return slides

@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=5000)  # Make sure to listen on all IP addresses
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))