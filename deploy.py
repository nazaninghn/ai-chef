"""
🚀 AI Chef Bot Deployment Helper
This script helps you deploy your AI Chef Bot to Streamlit Cloud
"""

import os
import subprocess
import webbrowser
from pathlib import Path

def check_files():
    """Check if all required files are present"""
    required_files = [
        'chef_bot_huggingface.py',
        'requirement.txt',
        'README.md',
        '.gitignore'
    ]
    
    print("📋 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {missing_files}")
        return False
    
    # Check if .env exists but warn about it
    if os.path.exists('.env'):
        print("⚠️ .env file found - Make sure it's in .gitignore!")
    
    print("\n✅ All required files are present!")
    return True

def check_git():
    """Check if git is initialized"""
    if os.path.exists('.git'):
        print("✅ Git repository initialized")
        return True
    else:
        print("❌ Git not initialized")
        return False

def init_git():
    """Initialize git repository"""
    try:
        subprocess.run(['git', 'init'], check=True)
        print("✅ Git repository initialized")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to initialize git")
        return False
    except FileNotFoundError:
        print("❌ Git not installed. Please install Git first.")
        return False

def show_deployment_steps():
    """Show step-by-step deployment instructions"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT STEPS")
    print("="*60)
    
    print("\n📋 STEP 1: Create GitHub Repository")
    print("1. Go to https://github.com")
    print("2. Click '+' → 'New repository'")
    print("3. Repository name: 'ai-chef-bot'")
    print("4. Description: '🤖🍳 AI-powered cooking assistant'")
    print("5. Make it PUBLIC")
    print("6. Click 'Create repository'")
    
    print("\n📤 STEP 2: Upload Files to GitHub")
    print("1. In your new repository, click 'uploading an existing file'")
    print("2. Drag and drop these files:")
    print("   ✅ chef_bot_huggingface.py")
    print("   ✅ requirement.txt")
    print("   ✅ README.md")
    print("   ✅ .gitignore")
    print("   ✅ run_chef_bot.py")
    print("   ❌ DON'T upload .env (contains your API key!)")
    print("3. Commit message: 'Add AI Chef Bot'")
    print("4. Click 'Commit changes'")
    
    print("\n🌐 STEP 3: Deploy to Streamlit Cloud")
    print("1. Go to https://share.streamlit.io")
    print("2. Sign in with your GitHub account")
    print("3. Click 'New app'")
    print("4. Select your repository: 'ai-chef-bot'")
    print("5. Main file path: 'chef_bot_huggingface.py'")
    print("6. Click 'Deploy'")
    
    print("\n🔑 STEP 4: Add Your API Key")
    print("1. In Streamlit Cloud, go to your app")
    print("2. Click 'Settings' → 'Secrets'")
    print("3. Add this line:")
    print("   HUGGINGFACE_API_KEY = \"your_actual_token_here\"")
    print("4. Click 'Save'")
    
    print("\n🎉 STEP 5: Your App is Live!")
    print("You'll get a URL like: https://your-app-name.streamlit.app")
    print("Share it with friends and family!")
    
    print("\n" + "="*60)

def open_helpful_links():
    """Open helpful links in browser"""
    print("\n🔗 Opening helpful links...")
    
    links = [
        ("GitHub", "https://github.com"),
        ("Streamlit Cloud", "https://share.streamlit.io"),
        ("HuggingFace Tokens", "https://huggingface.co/settings/tokens")
    ]
    
    for name, url in links:
        try:
            webbrowser.open(url)
            print(f"✅ Opened {name}")
        except:
            print(f"❌ Could not open {name}: {url}")

def main():
    print("🤖🍳 AI Chef Bot Deployment Helper")
    print("="*50)
    
    # Check files
    if not check_files():
        print("\n❌ Please fix missing files before deployment")
        return
    
    # Check git
    if not check_git():
        print("\n🔧 Initializing git repository...")
        if not init_git():
            print("❌ Could not initialize git")
            return
    
    # Show deployment steps
    show_deployment_steps()
    
    # Ask if user wants to open links
    print("\n" + "="*60)
    response = input("🔗 Open helpful links in browser? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        open_helpful_links()
    
    print("\n🎯 Next Steps:")
    print("1. Follow the steps above")
    print("2. Upload your files to GitHub")
    print("3. Deploy to Streamlit Cloud")
    print("4. Add your HuggingFace API key")
    print("5. Share your live app!")
    
    print("\n🤖🍳 Good luck with your deployment!")

if __name__ == "__main__":
    main()