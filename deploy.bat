@echo off
echo ========================================
echo   DocuMate - Streamlit Deployment Setup
echo ========================================
echo.

echo Step 1: Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not found. Install from https://git-scm.com/
    pause
    exit /b
)
echo ✓ Git installed

echo.
echo Step 2: Initialize Git repository...
if not exist .git (
    git init
    echo ✓ Git initialized
) else (
    echo ✓ Git already initialized
)

echo.
echo Step 3: Add files to Git...
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
echo ✓ Files committed

echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo.
echo 1. Create GitHub repository at https://github.com/new
echo    Name it: DocuMate
echo.
echo 2. Run these commands (replace YOUR_USERNAME):
echo    git remote add origin https://github.com/YOUR_USERNAME/DocuMate.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Go to https://share.streamlit.io
echo    - Click "New app"
echo    - Select your DocuMate repository
echo    - Main file: streamlit_app.py
echo    - Add secrets (see DEPLOYMENT.md)
echo.
echo 4. Your app will be live in 2-3 minutes!
echo.
pause
