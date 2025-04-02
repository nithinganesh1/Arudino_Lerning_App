from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = app = Flask(__name__, template_folder='templates')

# Mock data for chapters and lessons
chapters = [
    {"id": 1, "title": "LED Blinking", "lessons": [
        {"id": 1, "title": "What is an LED?"},
        {"id": 2, "title": "Connecting an LED"},
        {"id": 3, "title": "Writing the LED code"}
    ]},
    {"id": 2, "title": "Motors", "lessons": [
        {"id": 4, "title": "Introduction to Motors"},
        {"id": 5, "title": "Controlling Motor Speed"}
    ]}
]
@app.route('/')
def home():
    return render_template('index.html', chapters=chapters)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Chapter route
@app.route('/chapter/<int:chapter_id>')
def chapter(chapter_id):
    chapter = next((c for c in chapters if c["id"] == chapter_id), None)
    return render_template('chapter.html', chapter=chapter)

# Lesson route
@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    lesson = None
    for chapter in chapters:
        for l in chapter["lessons"]:
            if l["id"] == lesson_id:
                lesson = l
                break
    return render_template('lesson.html', lesson=lesson)

# Upload code to Arduino
@app.route('/upload', methods=['POST'])
def upload_code():
    code = request.json.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Ensure directory exists
    sketch_dir = "temp_sketch"
    os.makedirs(sketch_dir, exist_ok=True)

    # Save the file inside a folder with the same name
    sketch_path = os.path.join(sketch_dir, "temp_sketch.ino")
    with open(sketch_path, "w") as f:
        f.write(code)

    # Compile (not upload)
    try:
        result = subprocess.run(
            ["arduino-cli", "compile", "--fqbn", "arduino:avr:uno", sketch_dir],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return jsonify({"message": "Compilation successful!"})
        else:
            return jsonify({"error": result.stderr}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)