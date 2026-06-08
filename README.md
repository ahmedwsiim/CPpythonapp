# True Flask App

This repository contains a minimal, clean Flask application with a small frontend, tests, and a GitHub Actions CI workflow.

Getting started

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the app locally:

```bash
python -m app.main
# then open http://localhost:8000
```

3. Run tests:

```bash
pytest
```

Push to GitHub

1. Create a new repository on GitHub (via the website).
2. On your machine, initialize git, commit, and add the remote, then push:

```bash
git init
git add .
git commit -m "Initial minimal Flask app"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

After you push, GitHub Actions will run the CI workflow defined in `.github/workflows/ci.yml`.

If you want help creating the GitHub repo or pushing with a token or `gh` CLI, tell me and I can provide commands.
