import os
from flask import Flask, render_template

app = Flask(__name__)

def get_related_images(image_group):
    """Find all images for a scam type"""
    image_dir = os.path.join('static', 'images', image_group)
    if not os.path.exists(image_dir):
        return []
    
    images = []
    for file in os.listdir(image_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            images.append({
                'path': f'images/{image_group}/{file}',
                'name': os.path.splitext(file)[0].replace('_', ' ').title()
            })
    return images

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
                    image_group = line.lower()
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'image_group': image_group,
                        'images': get_related_images(image_group)  # Add images here
                    }
                elif current_slide:
                    current_slide['content'].append(line)
        
        if current_slide:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        slides = [{
            'title': 'Demo Slide',
            'content': ['Sample content'],
            'images': [{
                'path': 'images/error.jpg',
                'name': 'Demo Image'
            }]
        }]
    
    return slides

@app.route('/')
def index():
    slides = parse_slides()
    return render_template('index.html', slides=slides)
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