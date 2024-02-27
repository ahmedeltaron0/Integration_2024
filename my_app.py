from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def page1():
    return render_template('video.html')

@app.route('/audio')
def page2():
    return render_template('audio.html')

@app.route('/text')
def page3():
    return render_template('text.html')

if __name__ == '__main__':
    app.run(debug=True)
