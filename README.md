---
title: 'Alt Text Mage'
emoji: '🖼️'
colorFrom: 'pink'
colorTo: 'purple'
sdk: 'docker'
app_file: 'app.py'
pinned: false
---

# Alt Text Genie - Backend
The backend for Alt Text Mage, an AI/ML-powered alt text generator that allows bloggers and content editors to quickly generate alt text for better accessibility and SEO.

## Stack

- Python
- Fast API
- Supabase(Auth and Storage)
- Stripe
- Hugging Face Transformer
- BLIP model


# Install and Setup
Enter the following commands in zsh terminal:
```
python -m venv .env

source .env/bin/activate

pip install -r requirements.txt

python app.py
```
