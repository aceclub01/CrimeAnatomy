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
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'images': []  # Initialize images array
                    }
                elif line.startswith('[IMAGE:') and line.endswith(']'):
                    if current_slide:
                        img_name = line[7:-1].strip()  # Extract "loneliness.jpg"
                        current_slide['images'].append(img_name)
                elif current_slide:
                    current_slide['content'].append(line)
        
        if current_slide:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        slides = [{
            'title': 'Debug Slide',
            'content': ['Sample content'],
            'images': ['demo.jpg']
        }]
    
    return slides
    slides = []
    current_slide = None
    
    try:
        with open('slides.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            print(f"DEBUG: Read {len(lines)} lines from slides.txt")  # Debug output
            
            for line in lines:
                line = line.strip()
                print(f"DEBUG: Processing line: '{line}'")  # Show each line being processed
                
                # Skip empty lines unless they separate slides
                if not line:
                    if current_slide and current_slide['content']:
                        slides.append(current_slide)
                        current_slide = None
                    continue
                
                # Detect new section
                if line.lower().endswith('_scams'):
                    if current_slide:
                        slides.append(current_slide)
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'content': [],
                        'images': []
                    }
                # Detect image markers
                elif line.startswith('[IMAGE:'):
                    if current_slide:
                        img = line[7:-1].strip()  # Extract 'loneliness.jpg' from [IMAGE: loneliness.jpg]
                        current_slide['images'].append(img)
                # Add all other content
                elif current_slide:
                    current_slide['content'].append(line)
        
        # Add the last slide
        if current_slide and current_slide['content']:
            slides.append(current_slide)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        slides = [{
            'title': 'Debug Slide',
            'content': ['Sample content line 1', 'Sample content line 2'],
            'images': ['demo.jpg']
        }]
    
    # Debug output
    print(f"DEBUG: Parsed {len(slides)} slides:")
    for i, slide in enumerate(slides):
        print(f"Slide {i+1}: {slide['title']}")
        print(f"Content: {slide['content']}")
        print(f"Images: {slide['images']}\n")
    
    return slides
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