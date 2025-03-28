import os
from flask import Flask, render_template

app = Flask(__name__)

def load_introduction(scam_type):
    """Load introduction from external file"""
    filename = f"slides_{scam_type}.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return f"Introduction to {scam_type.replace('_', ' ')} not available."

def parse_slides():
    slides = []
    current_slide = None
    
    try:
        with open('slides.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                if not line:
                    if current_slide:
                        slides.append(current_slide)
                        current_slide = None
                    continue
                
                if line.lower().endswith('_scams'):
                    scam_type = line.replace('_scams', '').lower()
                    if current_slide:
                        slides.append(current_slide)
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'introduction': load_introduction(scam_type),
                        'content': [],
                        'images': []
                    }
                elif line.startswith('[IMAGE:') and line.endswith(']'):
                    if current_slide:
                        img_name = line[7:-1].strip()
                        current_slide['images'].append(img_name)
                elif current_slide:
                    current_slide['content'].append(line)
        
        if current_slide:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        slides = [{
            'title': 'Debug Slide',
            'introduction': 'Sample introduction',
            'content': ['Sample content'],
            'images': ['demo.jpg']
        }]
    
    return slides

@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)