import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

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
                    if current_slide:
                        slides.append(current_slide)
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'images': []
                    }
                elif line.startswith('[IMAGE:') and line.endswith(']'):
                    if current_slide:
                        img_name = line[7:-1].strip()
                        current_slide['images'].append({
                            'desktop': f'images/{img_name}',
                            'mobile': f'images/mobile/{img_name}'
                        })
                elif current_slide:
                    current_slide['content'].append(line)
        
        if current_slide:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        slides = [{
            'title': 'Debug Slide',
            'content': ['Content failed to load'],
            'images': [{
                'desktop': 'images/error.jpg',
                'mobile': 'images/mobile/error.jpg'
            }]
        }]
    
    return slides

@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

@app.route('/service-worker.js')
def sw():
    return send_from_directory('static', 'js/service-worker.js')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)