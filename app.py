import markupsafe
markupsafe.soft_unicode = markupsafe.soft_str  # Compatibility fix
import os
from flask import Flask, render_template



app = Flask(__name__)

from flask import Markup  # Add to top of file

def load_introduction(scam_type):
    """Load and properly format introduction content with enhanced highlighting"""
    filename = f"slides_{scam_type}.txt"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            highlighted_paras = []
            
            # Enhanced keyword lists for different categories
            danger_keywords = ['scam', 'fraud', 'exploit', 'vulnerability', 'danger', 'risk']
            financial_keywords = ['money', 'financial', 'emergency', 'funds', 'payment']
            psychological_keywords = ['loneliness', 'isolation', 'desire', 'connection', 
                                    'cognitive dissonance', 'idealism', 'emotional']
            tactic_keywords = ['fake profiles', 'stolen photos', 'love bombing', 
                             'constant communication', 'fabricate', 'disappear']
            
            for para in paragraphs:
                # Process bullet points and lists
                if para.startswith(('1.', '2.', '3.', '- ', '✓ ', '• ')):
                    lines = para.split('\n')
                    processed_lines = []
                    for line in lines:
                        # Highlight different categories with different colors
                        line = highlight_keywords(line, danger_keywords, 'danger-highlight')
                        line = highlight_keywords(line, financial_keywords, 'financial-highlight')
                        line = highlight_keywords(line, psychological_keywords, 'psych-highlight')
                        line = highlight_keywords(line, tactic_keywords, 'tactic-highlight')
                        
                        processed_lines.append(f"<li>{line[2:] if line[:2] in ('1.', '2.', '3.', '- ', '✓ ', '• ') else line}</li>")
                    highlighted_paras.append(f"<ul>{''.join(processed_lines)}</ul>")
                else:
                    # Process regular paragraphs
                    para = highlight_keywords(para, danger_keywords, 'danger-highlight')
                    para = highlight_keywords(para, financial_keywords, 'financial-highlight')
                    para = highlight_keywords(para, psychological_keywords, 'psych-highlight')
                    para = highlight_keywords(para, tactic_keywords, 'tactic-highlight')
                    highlighted_paras.append(f"<p>{para}</p>")
            
            return Markup('\n'.join(highlighted_paras))
            
    except Exception as e:
        return Markup(f"<p class='error'>Introduction loading error: {str(e)}</p>")

def highlight_keywords(text, keywords, css_class):
    """Helper function to highlight keywords with specified CSS class"""
    for kw in keywords:
        if kw.lower() in text.lower():
            # Case-insensitive replacement while preserving original case
            start_idx = text.lower().find(kw.lower())
            original_word = text[start_idx:start_idx+len(kw)]
            text = text.replace(original_word, f'<span class="{css_class}">{original_word}</span>')
    return text
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