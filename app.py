import markupsafe
markupsafe.soft_unicode = markupsafe.soft_str  # Compatibility fix
import os
from flask import Flask, render_template



app = Flask(__name__)

from flask import Markup  # Add to top of file

def load_introduction(scam_type):
    """Load and properly format introduction content"""
    filename = f"slides_{scam_type}.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
            # First convert to proper paragraphs
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            
            # Then apply highlighting to each paragraph
            highlighted_paras = []
            keywords = ['scam', 'fraud', 'warning', 'danger', 'risk', 'emergency', 
                       'financial', 'exploit', 'vulnerability']
            
            for para in paragraphs:
                # Process bullet points and lists
                if para.startswith(('1.', '2.', '3.', '- ', '✓ ', '• ')):
                    lines = para.split('\n')
                    processed_lines = []
                    for line in lines:
                        for kw in keywords:
                            if kw in line.lower():
                                line = line.replace(kw, f'<span class="highlight">{kw}</span>')
                        processed_lines.append(f"<li>{line[2:] if line[:2] in ('1.', '2.', '3.', '- ', '✓ ', '• ') else line}</li>")
                    highlighted_paras.append(f"<ul>{''.join(processed_lines)}</ul>")
                else:
                    # Process regular paragraphs
                    for kw in keywords:
                        if kw in para.lower():
                            para = para.replace(kw, f'<span class="highlight">{kw}</span>')
                    highlighted_paras.append(f"<p>{para}</p>")
            
            return Markup('\n'.join(highlighted_paras))
            
    except Exception as e:
        return Markup(f"<p class='error'>Introduction loading error: {str(e)}</p>")
    """Load and format introduction with paragraphs and highlights"""
    filename = f"slides_{scam_type}.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
            # Convert newlines to HTML paragraphs and highlight keywords
            paragraphs = []
            for para in content.split('\n\n'):  # Double newline = new paragraph
                # Highlight scam-related keywords
                highlighted = para
                keywords = ['scam', 'fraud', 'warning', 'danger', 'risk']
                for word in keywords:
                    highlighted = highlighted.replace(
                        word, 
                        f'<span class="highlight">{word}</span>'
                    )
                paragraphs.append(f"<p>{highlighted}</p>")
            
            return '\n'.join(paragraphs)
            
    except Exception as e:
        return f"<p>Introduction loading error: {str(e)}</p>"
    """
    Load introduction content from external file
    Args:
        scam_type (str): The scam type (e.g., 'loveScam', 'MoneyScam')
    Returns:
        str: The introduction content or error message
    """
    filename = f"slides_{scam_type}.txt"
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                if not content:
                    return f"No content found in {filename}"
                return content
        else:
            return f"Introduction file not found: {filename}"
    except Exception as e:
        print(f"Error loading {filename}: {str(e)}")
        return f"Could not load introduction: {str(e)}"

def parse_slides():
    """
    Parse the main slides file and load associated introductions
    Returns:
        list: Processed slides with introductions
    """
    slides = []
    current_slide = None
    
    try:
        with open('slides.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                
                # Skip empty lines unless they separate slides
                if not line:
                    if current_slide:
                        slides.append(current_slide)
                        current_slide = None
                    continue
                
                # Detect new scam section
                if line.lower().endswith('_scams'):
                    scam_type = line.replace('_scams', '').lower()
                    if current_slide:
                        slides.append(current_slide)
                    
                    # Create new slide with introduction
                    current_slide = {
                        'title': line.replace('_scams', ' Scams').title(),
                        'introduction': load_introduction(scam_type),
                        'content': [],
                        'images': [],
                        'scam_type': scam_type  # Store for debugging
                    }
                
                # Detect image markers
                elif line.startswith('[IMAGE:') and line.endswith(']'):
                    if current_slide:
                        img_name = line[7:-1].strip()
                        current_slide['images'].append(img_name)
                
                # Add regular content
                elif current_slide:
                    current_slide['content'].append(line)
        
        # Add the last slide if exists
        if current_slide:
            slides.append(current_slide)
            
    except FileNotFoundError:
        print("Error: slides.txt file not found")
        slides = [{
            'title': 'Error',
            'introduction': 'Could not load slides.txt',
            'content': ['Please check the file exists'],
            'images': []
        }]
    except Exception as e:
        print(f"Error parsing slides: {str(e)}")
        slides = [{
            'title': 'Error',
            'introduction': 'An error occurred',
            'content': [f'System error: {str(e)}'],
            'images': []
        }]
    
    # Debug output
    print(f"Loaded {len(slides)} slides")
    for i, slide in enumerate(slides, 1):
        print(f"Slide {i}: {slide['title']}")
        print(f"  Intro: {slide['introduction'][:50]}...")
        print(f"  Content lines: {len(slide['content'])}")
        print(f"  Images: {len(slide['images'])}")
    
    return slides

@app.route('/')
def index():
    """Main route that renders the presentation"""
    slides = parse_slides()
    return render_template('index.html', slides=slides)

@app.route('/debug')
def debug():
    """Debug endpoint to check file loading"""
    slides = parse_slides()
    files = {
        'exists': {
            'slides.txt': os.path.exists('slides.txt'),
            'loveScam': os.path.exists('slides_loveScam.txt'),
            'moneyScam': os.path.exists('slides_MoneyScam.txt')
        },
        'slides': slides
    }
    return render_template('debug.html', files=files)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000, debug=True)