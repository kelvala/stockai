# Step-by-Step GitHub Deployment

## 1. Create Repository on GitHub.com
- Go to https://github.com
- Click "+" → "New repository" 
- Name: stockai
- Make it PUBLIC
- Don't initialize with files
- Click "Create repository"

## 2. Push Your Code
Replace YOUR_USERNAME with your actual GitHub username:

```bash
git remote add origin https://github.com/YOUR_USERNAME/stockai.git
git branch -M main
git push -u origin main
```

## 3. Deploy to Streamlit Cloud
- Go to https://share.streamlit.io
- Sign in with GitHub
- Click "New app"
- Select your stockai repository
- Main file: streamlit_app.py
- Click "Deploy!"

Your app will be live at: https://YOUR_APP_NAME.streamlit.app
