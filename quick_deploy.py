#!/usr/bin/env python3
"""
🚀 Quick Deploy - Get your AI Chef Bot live in 5 minutes!
"""

import webbrowser
import os
import subprocess
import sys

def check_git():
    """Check if git is available"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def init_git_repo():
    """Initialize git repository if not exists"""
    if not os.path.exists('.git'):
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit: AI Chef Bot'], check=True)
            print("✅ Git repository initialized!")
            return True
        except Exception as e:
            print(f"❌ Git setup failed: {e}")
            return False
    else:
        print("✅ Git repository already exists")
        return True

def show_streamlit_cloud_steps():
    """Show Streamlit Cloud deployment steps"""
    print("\n" + "="*60)
    print("🌐 STREAMLIT CLOUD DEPLOYMENT (100% FREE)")
    print("="*60)
    
    print("\n📋 STEP 1: Create GitHub Repository")
    print("1. Go to: https://github.com/new")
    print("2. Repository name: ai-chef-bot")
    print("3. Description: 🤖🍳 AI-powered cooking assistant")
    print("4. Make it PUBLIC ✅")
    print("5. Click 'Create repository'")
    
    print("\n📤 STEP 2: Upload Your Files")
    print("Upload these files to your GitHub repo:")
    print("✅ chef_bot_huggingface.py")
    print("✅ requirement.txt")
    print("✅ README.md")
    print("✅ app.py (for HuggingFace Spaces)")
    print("❌ DON'T upload .env (contains your API key!)")
    
    print("\n🚀 STEP 3: Deploy to Streamlit Cloud")
    print("1. Go to: https://share.streamlit.io")
    print("2. Sign in with your GitHub account")
    print("3. Click 'New app'")
    print("4. Repository: your-username/ai-chef-bot")
    print("5. Main file path: chef_bot_huggingface.py")
    print("6. Click 'Deploy!'")
    
    print("\n🔑 STEP 4: Add Your API Key")
    print("1. In your app dashboard, click 'Settings'")
    print("2. Go to 'Secrets' tab")
    print("3. Add this line:")
    print('   HUGGINGFACE_API_KEY = "your_actual_token_here"')
    print("4. Click 'Save'")
    print("5. Your app will restart automatically")
    
    print("\n🎉 STEP 5: Your App is Live!")
    print("Your app will be available at:")
    print("https://your-app-name.streamlit.app")
    print("Share this URL with anyone!")

def show_huggingface_spaces_steps():
    """Show HuggingFace Spaces deployment steps"""
    print("\n" + "="*60)
    print("🤗 HUGGINGFACE SPACES DEPLOYMENT (100% FREE)")
    print("="*60)
    
    print("\n📋 STEP 1: Create HuggingFace Space")
    print("1. Go to: https://huggingface.co/spaces")
    print("2. Click 'Create new Space'")
    print("3. Space name: ai-chef-bot")
    print("4. License: MIT")
    print("5. SDK: Streamlit")
    print("6. Hardware: CPU (free)")
    print("7. Click 'Create Space'")
    
    print("\n📤 STEP 2: Upload Files")
    print("Upload these files to your Space:")
    print("✅ app.py (main file)")
    print("✅ requirements.txt (rename from requirement.txt)")
    print("✅ README.md")
    
    print("\n🔑 STEP 3: Add Secrets")
    print("1. In your Space, go to 'Settings'")
    print("2. Click 'Repository secrets'")
    print("3. Add secret:")
    print("   Name: HUGGINGFACE_API_KEY")
    print("   Value: your_actual_token_here")
    print("4. Click 'Add secret'")
    
    print("\n🎉 Your app will be live at:")
    print("https://huggingface.co/spaces/your-username/ai-chef-bot")

def show_railway_steps():
    """Show Railway deployment steps"""
    print("\n" + "="*60)
    print("🚂 RAILWAY DEPLOYMENT ($5 FREE CREDITS)")
    print("="*60)
    
    print("\n📋 DEPLOYMENT STEPS:")
    print("1. Push your code to GitHub (public repo)")
    print("2. Go to: https://railway.app")
    print("3. Sign up with GitHub")
    print("4. Click 'New Project' → 'Deploy from GitHub repo'")
    print("5. Select your ai-chef-bot repository")
    print("6. Railway will auto-detect Streamlit!")
    print("7. Add environment variable:")
    print("   HUGGINGFACE_API_KEY = your_token")
    print("8. Deploy automatically!")

def open_deployment_sites():
    """Open deployment sites in browser"""
    sites = [
        ("GitHub", "https://github.com/new"),
        ("Streamlit Cloud", "https://share.streamlit.io"),
        ("HuggingFace Spaces", "https://huggingface.co/spaces"),
        ("Railway", "https://railway.app"),
        ("HuggingFace Tokens", "https://huggingface.co/settings/tokens")
    ]
    
    print("\n🔗 Opening deployment sites...")
    for name, url in sites:
        try:
            webbrowser.open(url)
            print(f"✅ Opened {name}")
        except:
            print(f"❌ Could not open {name}: {url}")

def main():
    print("🚀 QUICK DEPLOY - AI Chef Bot")
    print("="*50)
    print("Get your AI Chef Bot live in 5 minutes!")
    print()
    
    # Check git
    if not check_git():
        print("❌ Git not found. Please install Git first.")
        print("Download from: https://git-scm.com/downloads")
        return
    
    # Initialize git repo
    if not init_git_repo():
        print("❌ Could not set up git repository")
        return
    
    print("\n🎯 CHOOSE YOUR DEPLOYMENT PLATFORM:")
    print("1. 🌐 Streamlit Cloud (Recommended - Easiest)")
    print("2. 🤗 HuggingFace Spaces (Best for AI apps)")
    print("3. 🚂 Railway (Good performance)")
    print("4. 📋 Show all options")
    print("0. Just open the sites")
    
    choice = input("\nEnter your choice (0-4): ").strip()
    
    if choice == '1':
        show_streamlit_cloud_steps()
    elif choice == '2':
        show_huggingface_spaces_steps()
    elif choice == '3':
        show_railway_steps()
    elif choice == '4':
        show_streamlit_cloud_steps()
        show_huggingface_spaces_steps()
        show_railway_steps()
    elif choice == '0':
        pass
    else:
        print("Invalid choice, showing all options...")
        show_streamlit_cloud_steps()
    
    print("\n" + "="*60)
    response = input("🔗 Open deployment sites in browser? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        open_deployment_sites()
    
    print("\n🎯 QUICK CHECKLIST:")
    print("□ Create GitHub repository (public)")
    print("□ Upload files (except .env)")
    print("□ Choose deployment platform")
    print("□ Add HuggingFace API key to secrets")
    print("□ Deploy and share your app!")
    
    print("\n🤖🍳 Your AI Chef Bot will be live soon!")
    print("Good luck with your deployment! 🚀")

if __name__ == "__main__":
    main()