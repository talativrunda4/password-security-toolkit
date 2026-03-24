from flask import Flask, render_template, request, jsonify, session
import random
import string
from collections import deque
 
app = Flask(__name__)
app.secret_key = "password_toolkit_secret_key"
 
# ══════════════════════════════════════════════
#  Core Logic (same as app.py)
# ══════════════════════════════════════════════
 
def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
 
def check_strength(password):
    score = 0
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    elif len(password) >= 6:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2
    for pattern in ["123", "password", "abc", "qwerty", "111", "000"]:
        if pattern in password.lower():
            score -= 2
    return max(0, min(score, 10))
 
def analyze_password(password):
    score = check_strength(password)
    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    else:
        strength = "Strong"
    suggestions = []
    if len(password) < 8:
        suggestions.append("Use at least 8 characters")
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters (A-Z)")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters (a-z)")
    if not any(c.isdigit() for c in password):
        suggestions.append("Add digits (0-9)")
    if not any(c in string.punctuation for c in password):
        suggestions.append("Add special characters (!@#$...)")
    return strength, score, suggestions
 
# ══════════════════════════════════════════════
#  Routes
# ══════════════════════════════════════════════
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.get_json()
    length = int(data.get('length', 12))
    length = max(8, min(64, length))
    password = generate_password(length)
    strength, score, suggestions = analyze_password(password)
    return jsonify({'password': password, 'strength': strength, 'score': score})
 
@app.route('/api/check', methods=['POST'])
def api_check():
    data = request.get_json()
    password = data.get('password', '')
    if not password:
        return jsonify({'error': 'Password cannot be empty'}), 400
    strength, score, suggestions = analyze_password(password)
 
    # Save to session history
    if 'history' not in session:
        session['history'] = []
    masked = password[:2] + '*' * (len(password) - 4) + password[-2:] if len(password) > 4 else password
    entry = {'masked': masked, 'strength': strength, 'score': score}
    history = session['history']
    history.append(entry)
    session['history'] = history[-3:]  # keep last 3
 
    return jsonify({'strength': strength, 'score': score, 'suggestions': suggestions})
 
@app.route('/api/history')
def api_history():
    return jsonify({'history': session.get('history', [])})
 
if __name__ == '__main__':
    app.run(debug=True)