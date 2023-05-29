import os
import subprocess
import shutil
import hashlib
from flask import Flask, request

app = Flask(__name__)

# Get the repository URL from environment variable
repo_url = os.environ.get('REPO_URL')
webhook_secret = os.environ.get('WEBHOOK_SECRET')

print(f"Repository URL: {repo_url}")
print(f"Webhook secret: {webhook_secret}")

def hash_secret(secret):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(secret.encode('utf-8'))
    return sha1_hash.hexdigest()

def pull_repo():
    if not os.path.exists('./repository'):
        # Clone the repository if it doesn't exist locally
        subprocess.run(['git', 'clone', repo_url, './repository'])
    else: 
        # Check if the existing repository matches the desired URL
        result = subprocess.run(['git', '-C', './repository', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        existing_repo_url = result.stdout.strip()
        
        if existing_repo_url == repo_url:
            # Pull the latest changes if the repository already exists and matches the desired URL
            subprocess.run(['git', '-C', './repository', 'pull'])
        else:
            # Remove the existing repository content and clone the desired repository if they don't match
            shutil.rmtree('./repository/*', ignore_errors=True)
            subprocess.run(['git', 'clone', repo_url, './repository'])

@app.route('/webhook', methods=['POST'])
def webhook():
    event_type = request.headers.get('X-GitHub-Event')
    hashed_secret = hash_secret(webhook_secret)

    if event_type == 'push' and request.headers.get('X-Hub-Signature') == f'sha1={hashed_secret}':
        # Pull the repository if it's a push event on the main branch
        payload = request.get_json()
        if payload.get('ref') == 'refs/heads/main':
            print("Pulling repository...")
            pull_repo()
            return 'Updated repo', 200

    return 'Didnt update', 200

if __name__ == '__main__':
    # Pull the repository on startup
    pull_repo()

    # Start the Flask application
    app.run(host='0.0.0.0', port=5000)