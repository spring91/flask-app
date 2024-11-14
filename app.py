from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Vote tracking
votes = {"yes": 0, "no": 0}
voters = set()  # Track unique voters
vote_limit = 4  # Number of unique votes to trigger results

@app.route('/')
def home():
    """Render the voting interface."""
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    """Handle voting and return results when the limit is reached."""
    global votes, voters

    # Identify the voter using their IP address
    user_id = request.remote_addr

    # Check if the user has already voted
    if user_id in voters:
        return jsonify({"message": "You have already voted."}), 403

    # Process the vote
    data = request.json
    vote = data.get('vote', '').lower()
    if vote not in ["yes", "no"]:
        return jsonify({"error": "Invalid vote. Only 'yes' or 'no' allowed."}), 400

    # Register the vote
    votes[vote] += 1
    voters.add(user_id)

    # Check if the vote limit has been reached
    if len(voters) >= vote_limit:
        result = calculate_result()
        votes = {"yes": 0, "no": 0}  # Reset votes for future use
        voters.clear()  # Reset voter tracking
        return jsonify({"message": "Voting is closed.", "result": result})

    return jsonify({"message": "Vote received. Waiting for more votes."})

def calculate_result():
    """Calculate and return the result."""
    if votes["no"] > 0:  # Any "no" vote triggers a "no" result
        return "no"
    return "yes"  # All "yes" votes otherwise result in "yes"

if __name__ == "__main__":
    app.run(debug=True)
