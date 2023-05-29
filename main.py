import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Get the repository URL from environment variable
repo_url = os.environ.get('REPO_URL')
webhook_secret = os.environ.get('WEBHOOK_SECRET')

def pull_repo():
    if not os.path.exists('./repository'):
        # Clone the repository if it doesn't exist locally
        subprocess.run(['git', 'clone', repo_url, './repository'])
        
        # Check if the existing repository matches the desired URL
        result = subprocess.run(['git', '-C', './repository', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        existing_repo_url = result.stdout.strip()
        
        if existing_repo_url == repo_url:
            # Pull the latest changes if the repository already exists and matches the desired URL
            subprocess.run(['git', '-C', './repository', 'pull'])
        else:
            # Remove the existing repository and clone the desired repository if they don't match
            shutil.rmtree('./repository')
            subprocess.run(['git', 'clone', repo_url, './repository'])

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    secret = 'your_secret'  # Set your secret here

    if event_type == 'push' and request.headers.get('X-Hub-Signature') == secret:
        # Pull the repository if it's a push event on the main branch
        payload = request.get_json()
        if payload.get('ref') == 'refs/heads/main':
            pull_repo()

    return 'Webhook received', 200

if __name__ == '__main__':
    # Pull the repository on startup
    pull_repo()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)