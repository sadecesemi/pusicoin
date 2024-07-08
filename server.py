from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = 'scores.json'

def load_scores():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_scores(scores):
    with open(DATA_FILE, 'w') as f:
        json.dump(scores, f)

@app.route('/update_score', methods=['POST'])
def update_score():
    data = request.json
    score = data.get('score')
    user_id = data.get('user_id')

    if score is not None and user_id:
        scores = load_scores()
        scores[user_id] = score
        save_scores(scores)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'fail'}), 400

@app.route('/get_score/<user_id>', methods=['GET'])
def get_score(user_id):
    scores = load_scores()
    score = scores.get(user_id, 0)
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True)