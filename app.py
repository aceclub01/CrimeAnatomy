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
    """Robust slide parser with detailed error handling"""
    filepath = get_file_path('slides.txt')
    if not filepath:
        error_msg = "slides.txt not found in:\n- " + "\n- ".join([
            os.path.join(app.root_path, 'slides.txt'),
            os.path.join(os.getcwd(), 'slides.txt'),
            'slides.txt'
        ])
        print(error_msg)
        return [{
            'title': 'File Not Found',
            'content': [error_msg],
            'image_group': 'error'
        }]

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"File content (first 100 chars): {content[:100]}...")  # Debug output
            
            slides = []
            current_slide = None
            
            for line in content.splitlines():
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
                        'image_group': line.lower()
                    }
                elif current_slide:
                    current_slide['content'].append(line)
            
            if current_slide:
                slides.append(current_slide)
            
            print(f"Successfully parsed {len(slides)} slides")  # Debug
            return slides

    except Exception as e:
        error_msg = f"Error reading slides.txt: {str(e)}"
        print(error_msg)
        return [{
            'title': 'Parse Error',
            'content': [error_msg],
            'image_group': 'error'
        }]

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