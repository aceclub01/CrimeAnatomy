import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def get_file_path(filename):
    """Get absolute path to file, checking multiple locations"""
    paths_to_check = [
        os.path.join(app.root_path, filename),  # Standard Flask location
        os.path.join(os.getcwd(), filename),    # Current working directory
        filename                                # Direct path
    ]
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"Found file at: {path}")  # This will appear in Render logs
            return path
    return None

def parse_slides():
    slides = []
    current_slide = None
    
    try:
        with open('slides.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines unless they separate slides
                if not line:
                    if current_slide and current_slide['content']:  # Only add if has content
                        slides.append(current_slide)
                        current_slide = None
                    continue
                
                # Detect new section header
                if line.lower().endswith('_scams'):
                    if current_slide:  # Save previous slide if exists
                        slides.append(current_slide)
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'image_group': line.lower()
                    }
                elif current_slide:
                    # Add ALL content lines (not just special markers)
                    current_slide['content'].append(line)
        
        # Add the last slide if it exists
        if current_slide and current_slide['content']:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error loading slides: {str(e)}")
        slides = [{
            'title': 'Debug: Sample Slide',
            'content': [
                'This is sample content line 1',
                '🚩 This is a sample red flag',
                '"This is a sample question?"',
                'Regular content line without markers'
            ],
            'image_group': 'demo'
        }]
    
    print("DEBUG - Parsed Slides:")
    for i, slide in enumerate(slides):
        print(f"Slide {i+1}: {slide['title']}")
        for item in slide['content']:
            print(f" - {item}")
    
    return slides
@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)

@app.route('/debug')
def debug():
    """Comprehensive debug endpoint"""
    debug_info = {
        'current_directory': os.getcwd(),
        'files_in_root': os.listdir('.'),
        'flask_root_path': app.root_path,
        'slides_txt_path': get_file_path('slides.txt'),
        'slides_sample': parse_slides()[:1]  # First slide only
    }
    return jsonify(debug_info)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)