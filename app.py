from flask import Flask, render_template, request

from pca import batch_pca

app = Flask(__name__)
DATA_PATH = 'static'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    file = request.files['input']
    ext = file.content_type
    if file.filename != '' and ext in ['image/jpeg', 'image/png']:
        tail = file.filename.split('.')[-1]
        path = f'{DATA_PATH}/original.{tail}'
        file.save(path)
        w, pc = batch_pca(path)
    return render_template('result.html', original=path, w=w, pc=pc)

if __name__ == "__main__":
    app.run(debug=True)