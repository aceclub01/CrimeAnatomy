from flask import Flask, render_template

app = Flask(__name__)

def read_slides():
    slides = []
    try:
        with open("slides.txt", "r", encoding="utf-8") as file:
            slide = []
            for line in file:
                line = line.strip()
                if not line:
                    if slide:
                        slides.append(slide)
                        slide = []
                else:
                    slide.append(line)
            if slide:
                slides.append(slide)
    except FileNotFoundError:
        print("slides.txt not found!")
    return slides

@app.route('/')
def index():
    slides = read_slides()
    return render_template('index.html', slides=slides)

if __name__ == '__main__':
    app.run(debug=True)
