#!/usr/bin/env python3
"""
🆓 Free Server Deployment Guide for AI Chef Bot
Deploy your Streamlit app on completely free platforms
"""

import webbrowser
import os

def deploy_streamlit_cloud():
    """Streamlit Cloud - Best free option"""
    print("🌐 STREAMLIT CLOUD (100% FREE)")
    print("="*50)
    print("✅ Completely free forever")
    print("✅ Easy GitHub integration")
    print("✅ Automatic deployments")
    print("✅ Custom domain support")
    print()
    
    print("📋 DEPLOYMENT STEPS:")
    print("1. Push your code to GitHub:")
    print("   - Create new repo: 'ai-chef-bot'")
    print("   - Upload all files EXCEPT .env")
    print("   - Make repo PUBLIC")
    print()
    print("2. Deploy to Streamlit Cloud:")
    print("   - Go to: https://share.streamlit.io")
    print("   - Sign in with GitHub")
    print("   - Click 'New app'")
    print("   - Select your repo: ai-chef-bot")
    print("   - Main file: chef_bot_huggingface.py")
    print("   - Click 'Deploy'")
    print()
    print("3. Add your HuggingFace API key:")
    print("   - In app settings → Secrets")
    print('   - Add: HUGGINGFACE_API_KEY = "your_token"')
    print("   - Save and restart")
    print()
    print("🎉 Your app will be live at:")
    print("https://your-app-name.streamlit.app")

def deploy_railway():
    """Railway - Great free tier"""
    print("\n🚂 RAILWAY (FREE TIER)")
    print("="*50)
    print("✅ $5 free credits monthly")
    print("✅ Automatic deployments")
    print("✅ Custom domains")
    print("✅ Easy environment variables")
    print()
    
    print("📋 DEPLOYMENT STEPS:")
    print("1. Push code to GitHub (public repo)")
    print()
    print("2. Deploy on Railway:")
    print("   - Go to: https://railway.app")
    print("   - Sign up with GitHub")
    print("   - Click 'New Project'")
    print("   - Select 'Deploy from GitHub repo'")
    print("   - Choose your ai-chef-bot repo")
    print()
    print("3. Configure environment:")
    print("   - Add variable: HUGGINGFACE_API_KEY")
    print("   - Value: your_token_here")
    print("   - Railway auto-detects Streamlit!")
    print()
    print("🎉 Your app will be live with Railway URL")

def deploy_render():
    """Render - Another free option"""
    print("\n🎨 RENDER (FREE TIER)")
    print("="*50)
    print("✅ Free tier available")
    print("✅ GitHub integration")
    print("✅ Custom domains")
    print("⚠️ May sleep after inactivity")
    print()
    
    print("📋 DEPLOYMENT STEPS:")
    print("1. Push code to GitHub")
    print()
    print("2. Deploy on Render:")
    print("   - Go to: https://render.com")
    print("   - Sign up with GitHub")
    print("   - Click 'New Web Service'")
    print("   - Connect your repo")
    print("   - Build Command: pip install -r requirement.txt")
    print("   - Start Command: streamlit run chef_bot_huggingface.py --server.port=$PORT --server.address=0.0.0.0")
    print()
    print("3. Add environment variables:")
    print("   - HUGGINGFACE_API_KEY = your_token")
    print()
    print("🎉 Your app will be live on Render")

def deploy_huggingface_spaces():
    """HuggingFace Spaces - Perfect for AI apps"""
    print("\n🤗 HUGGINGFACE SPACES (FREE)")
    print("="*50)
    print("✅ Completely free")
    print("✅ Perfect for AI apps")
    print("✅ Built-in GPU support")
    print("✅ Easy Streamlit deployment")
    print()
    
    print("📋 DEPLOYMENT STEPS:")
    print("1. Go to: https://huggingface.co/spaces")
    print("2. Click 'Create new Space'")
    print("3. Choose:")
    print("   - Space name: ai-chef-bot")
    print("   - License: MIT")
    print("   - SDK: Streamlit")
    print("   - Hardware: CPU (free)")
    print()
    print("4. Upload files:")
    print("   - app.py (rename chef_bot_huggingface.py)")
    print("   - requirements.txt")
    print("   - README.md")
    print()
    print("5. Add secrets:")
    print("   - Settings → Repository secrets")
    print("   - HUGGINGFACE_API_KEY = your_token")
    print()
    print("🎉 Your app will be live at:")
    print("https://huggingface.co/spaces/your-username/ai-chef-bot")

def create_github_instructions():
    """Create step-by-step GitHub setup"""
    print("\n📚 GITHUB SETUP GUIDE")
    print("="*50)
    
    print("1. Create GitHub Repository:")
    print("   - Go to: https://github.com")
    print("   - Click '+' → 'New repository'")
    print("   - Name: ai-chef-bot")
    print("   - Description: 🤖🍳 AI-powered cooking assistant")
    print("   - Make it PUBLIC (required for free deployments)")
    print("   - Click 'Create repository'")
    print()
    
    print("2. Upload Your Files:")
    print("   - Click 'uploading an existing file'")
    print("   - Drag and drop these files:")
    print("     ✅ chef_bot_huggingface.py")
    print("     ✅ requirement.txt")
    print("     ✅ README.md")
    print("     ✅ Procfile")
    print("     ✅ railway.json")
    print("     ❌ DON'T upload .env (contains secrets!)")
    print("   - Commit message: 'Add AI Chef Bot'")
    print("   - Click 'Commit changes'")
    print()
    
    print("3. Your repo is ready for deployment!")

def main():
    print("🆓 FREE SERVER DEPLOYMENT OPTIONS")
    print("="*60)
    print("Deploy your AI Chef Bot on these FREE platforms:")
    print()
    
    # Show all free options
    deploy_streamlit_cloud()
    deploy_railway()
    deploy_render()
    deploy_huggingface_spaces()
    create_github_instructions()
    
    print("\n🎯 RECOMMENDED ORDER:")
    print("1. 🌐 Streamlit Cloud (easiest)")
    print("2. 🤗 HuggingFace Spaces (best for AI)")
    print("3. 🚂 Railway (good features)")
    print("4. 🎨 Render (backup option)")
    
    print("\n🔗 Want me to open these sites?")
    response = input("Open deployment sites in browser? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        sites = [
            "https://share.streamlit.io",
            "https://railway.app", 
            "https://render.com",
            "https://huggingface.co/spaces",
            "https://github.com"
        ]
        
        for site in sites:
            try:
                webbrowser.open(site)
                print(f"✅ Opened {site}")
            except:
                print(f"❌ Could not open {site}")
    
    print("\n🚀 Next Steps:")
    print("1. Choose a platform above")
    print("2. Create GitHub repo (if needed)")
    print("3. Follow the deployment steps")
    print("4. Add your HuggingFace API key")
    print("5. Share your live app!")
    
    print("\n🤖🍳 Happy free deployment!")

if __name__ == "__main__":
    main()