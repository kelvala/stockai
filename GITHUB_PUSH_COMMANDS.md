# GitHub Push Commands for "stockai"

After creating your GitHub repository named "stockai", run these commands:

```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/stockai.git

# Push your code to GitHub
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

Example (if your username is "johndoe"):
```bash
git remote add origin https://github.com/johndoe/stockai.git
git branch -M main
git push -u origin main
```

## Repository Privacy Settings:

**For Private Repository:**
- Create as private initially
- You can make it public later in Settings → General → Danger Zone → Change visibility

**For Streamlit Cloud Deployment:**
- Free tier requires public repositories
- If private, you'll need GitHub Pro/Team or make it public for deployment
