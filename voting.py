from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Anonymous vote counter
votes = {"yes": 0, "no": 0}
vote_limit = 4

@app.route('/')
def home():
    """Render the voting interface."""
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    """Handle voting and return results when the limit is reached."""
    global votes

    # Check if the vote limit has been reached
    if sum(votes.values()) >= vote_limit:
        return jsonify({"message": "Voting is closed.", "result": calculate_result()})

    # Process the vote
    data = request.json
    vote = data.get('vote', '').lower()
    if vote not in ["yes", "no"]:
        return jsonify({"error": "Invalid vote. Only 'yes' or 'no' allowed."}), 400

    votes[vote] += 1

    # Check again after vote if the limit is reached
    if sum(votes.values()) >= vote_limit:
        result = calculate_result()
        votes = {"yes": 0, "no": 0}  # Reset votes for future use
        return jsonify({"message": "Voting is closed.", "result": result})

    return jsonify({"message": "Vote received."})

def calculate_result():
    """Calculate and return the result."""
    if votes["no"] > 0:
        return "no"
    return "yes"

if __name__ == "__main__":
    app.run(debug=True)
