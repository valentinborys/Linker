from flask import Flask, request, redirect, jsonify, render_template
import string, random

app = Flask(__name__)
db = {}
history = []

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.route('/')
def home():
    return render_template('index.html', history=history)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_id = generate_short_id()
    short_url = request.host_url + short_id
    db[short_id] = original_url
    history.append({'original': original_url, 'short': short_url})
    return render_template('index.html', short_url=short_url, history=history)

@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = db.get(short_id)
    if original_url:
        return redirect(original_url)
    return 'URL не найден', 404

if __name__ == '__main__':
    app.run(debug=True)
