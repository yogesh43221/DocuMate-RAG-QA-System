# Streamlit Cloud Deployment Guide

## Prerequisites
1. GitHub account
2. Streamlit Cloud account (free at share.streamlit.io)
3. MongoDB Atlas URI
4. Google Gemini API Key

## Step-by-Step Deployment

### 1. Prepare Repository
```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Streamlit deployment"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/DocuMate.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repository: `YOUR_USERNAME/DocuMate`
4. Set:
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.11

### 3. Add Secrets

In Streamlit Cloud dashboard:
1. Click on your app
2. Go to "Settings" → "Secrets"
3. Add:

```toml
GEMINI_API_KEY = "AIza..."
MONGODB_URI = "mongodb+srv://username:password@cluster.mongodb.net/"
```

### 4. Deploy!

Click "Deploy" and wait 2-3 minutes.

Your app will be live at: `https://your-app-name.streamlit.app`

## Troubleshooting

### Backend not connecting
- Check secrets are correctly added
- Verify MongoDB Atlas allows connections from 0.0.0.0/0

### Import errors
- Ensure all dependencies in requirements.txt
- Check Python version compatibility

### Timeout errors
- Streamlit Cloud has 1GB RAM limit
- Consider upgrading or optimizing chunk size

## Local Testing

```bash
# Test the deployment setup locally
python streamlit_app.py
```

## Updates

To update your deployed app:
```bash
git add .
git commit -m "Update"
git push
```

Streamlit Cloud auto-deploys on push!
