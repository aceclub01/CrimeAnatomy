import os
from flask import Flask, render_template

app = Flask(__name__)

def parse_slides():
    slides = []
    current_slide = None
    
    with open('slides.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
                
            # Detect new slide
            if line.endswith('_scams'):
                if current_slide:
                    slides.append(current_slide)
                current_slide = {
                    'title': line.replace('_scams', ' Scams').title(),
                    'content': [],
                    'image_group': line
                }
            elif current_slide:
                if line.startswith(('🚩', '"')) or any(char.isdigit() for char in line[:3]):
                    current_slide['content'].append(line)
                else:
                    current_slide['title'] += ": " + line
    
    if current_slide:
        slides.append(current_slide)
    
    return slides
    
@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)  # Added port for Render compatibility