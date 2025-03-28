import os
from flask import Flask, render_template

app = Flask(__name__)

def parse_slides():
    slides = []
    current_slide = None
    
    try:
        # Get the absolute path to slides.txt
        filepath = os.path.join(app.root_path, 'slides.txt')
        print(f"Looking for slides.txt at: {filepath}")  # Debug path
        
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines unless they separate slides
                if not line:
                    if current_slide:  # Finalize current slide
                        slides.append(current_slide)
                        current_slide = None
                    continue
                
                # Detect new slide marker
                if line.lower().endswith('_scams'):
                    if current_slide:  # Save previous slide
                        slides.append(current_slide)
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'image_group': line.lower()
                    }
                elif current_slide:
                    # Add content to current slide
                    current_slide['content'].append(line)
        
        # Add the last slide if exists
        if current_slide:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error loading slides: {str(e)}")
        # Fallback demo data
        slides = [{
            'title': 'Demo: Love Scams',
            'content': [
                'Example vulnerability: Loneliness',
                '🚩 Red flag: Moving too fast',
                '"Would I send money to someone I never met?"'
            ],
            'image_group': 'love_scams'
        }]
    
    print(f"Loaded {len(slides)} slides")  # Debug output
    return slides

@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

@app.route('/debug')
def debug():
    """Debug endpoint to check files and slides"""
    files = os.listdir(app.root_path)
    slides = parse_slides()
    return {
        'files_in_root': files,
        'slides_count': len(slides),
        'first_slide': slides[0] if slides else None,
        'app_root': app.root_path
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)