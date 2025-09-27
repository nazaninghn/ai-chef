#!/usr/bin/env python3
"""
🚀 AI Chef Bot Server Deployment Script
Deploy your AI Chef Bot to various platforms
"""

import os
import subprocess
import sys
import json
from pathlib import Path

class ServerDeployer:
    def __init__(self):
        self.project_name = "ai-chef-bot"
        self.main_file = "chef_bot_huggingface.py"
        
    def check_requirements(self):
        """Check if all required files exist"""
        required_files = [
            'chef_bot_huggingface.py',
            'requirement.txt',
            'README.md',
            '.gitignore'
        ]
        
        print("📋 Checking deployment requirements...")
        missing = []
        
        for file in required_files:
            if os.path.exists(file):
                print(f"✅ {file}")
            else:
                print(f"❌ {file} - MISSING!")
                missing.append(file)
        
        if missing:
            print(f"\n⚠️ Missing files: {missing}")
            return False
            
        print("✅ All required files present!")
        return True
    
    def create_streamlit_secrets(self):
        """Create Streamlit secrets template"""
        secrets_content = '''# Streamlit Cloud Secrets
# Add your HuggingFace API key here

HUGGINGFACE_API_KEY = "your_huggingface_token_here"
'''
        
        os.makedirs('.streamlit', exist_ok=True)
        with open('.streamlit/secrets.toml', 'w') as f:
            f.write(secrets_content)
        
        print("✅ Created .streamlit/secrets.toml template")
    
    def deploy_streamlit_cloud(self):
        """Instructions for Streamlit Cloud deployment"""
        print("\n" + "="*60)
        print("🌐 STREAMLIT CLOUD DEPLOYMENT")
        print("="*60)
        
        print("\n📋 STEP 1: Prepare Repository")
        print("1. Push your code to GitHub")
        print("2. Make sure .env is in .gitignore")
        print("3. Don't commit your API keys!")
        
        print("\n🌐 STEP 2: Deploy to Streamlit Cloud")
        print("1. Go to https://share.streamlit.io")
        print("2. Sign in with GitHub")
        print("3. Click 'New app'")
        print("4. Repository: your-username/ai-chef-bot")
        print("5. Main file: chef_bot_huggingface.py")
        print("6. Click 'Deploy'")
        
        print("\n🔑 STEP 3: Add Secrets")
        print("1. In your app dashboard, click 'Settings'")
        print("2. Go to 'Secrets' tab")
        print("3. Add your HuggingFace API key:")
        print('   HUGGINGFACE_API_KEY = "your_token_here"')
        print("4. Save and restart app")
        
        print("\n🎉 Your app will be live at:")
        print("https://your-app-name.streamlit.app")
    
    def deploy_docker(self):
        """Deploy using Docker"""
        print("\n" + "="*60)
        print("🐳 DOCKER DEPLOYMENT")
        print("="*60)
        
        print("\n📋 STEP 1: Build Docker Image")
        print("docker build -t ai-chef-bot .")
        
        print("\n🚀 STEP 2: Run Container")
        print("docker run -p 8501:8501 --env-file .env ai-chef-bot")
        
        print("\n🔧 STEP 3: Using Docker Compose")
        print("docker-compose up -d")
        
        print("\n🌐 Access your app at: http://localhost:8501")
    
    def deploy_heroku(self):
        """Instructions for Heroku deployment"""
        print("\n" + "="*60)
        print("🟣 HEROKU DEPLOYMENT")
        print("="*60)
        
        # Create Procfile
        with open('Procfile', 'w') as f:
            f.write('web: streamlit run chef_bot_huggingface.py --server.port=$PORT --server.address=0.0.0.0\n')
        
        print("✅ Created Procfile")
        
        print("\n📋 DEPLOYMENT STEPS:")
        print("1. Install Heroku CLI")
        print("2. heroku login")
        print("3. heroku create ai-chef-bot-app")
        print("4. heroku config:set HUGGINGFACE_API_KEY=your_token")
        print("5. git push heroku main")
        
        print("\n🎉 Your app will be live at:")
        print("https://ai-chef-bot-app.herokuapp.com")
    
    def deploy_railway(self):
        """Instructions for Railway deployment"""
        print("\n" + "="*60)
        print("🚂 RAILWAY DEPLOYMENT")
        print("="*60)
        
        # Create railway.json
        railway_config = {
            "build": {
                "builder": "NIXPACKS"
            },
            "deploy": {
                "startCommand": "streamlit run chef_bot_huggingface.py --server.port=$PORT --server.address=0.0.0.0",
                "healthcheckPath": "/_stcore/health",
                "healthcheckTimeout": 100,
                "restartPolicyType": "ON_FAILURE",
                "restartPolicyMaxRetries": 10
            }
        }
        
        with open('railway.json', 'w') as f:
            json.dump(railway_config, f, indent=2)
        
        print("✅ Created railway.json")
        
        print("\n📋 DEPLOYMENT STEPS:")
        print("1. Go to https://railway.app")
        print("2. Sign up with GitHub")
        print("3. Click 'New Project' → 'Deploy from GitHub repo'")
        print("4. Select your repository")
        print("5. Add environment variable:")
        print("   HUGGINGFACE_API_KEY = your_token")
        print("6. Deploy automatically!")
        
        print("\n🎉 Your app will be live with a Railway URL")
    
    def show_menu(self):
        """Show deployment options menu"""
        print("\n🚀 AI Chef Bot Server Deployment")
        print("="*50)
        print("Choose your deployment platform:")
        print()
        print("1. 🌐 Streamlit Cloud (Recommended - Free)")
        print("2. 🐳 Docker (Local/VPS)")
        print("3. 🟣 Heroku (Paid)")
        print("4. 🚂 Railway (Free tier)")
        print("5. 📋 Show all options")
        print("0. Exit")
        print()
        
        choice = input("Enter your choice (0-5): ").strip()
        return choice
    
    def run(self):
        """Main deployment runner"""
        print("🤖🍳 AI Chef Bot Server Deployment Helper")
        
        if not self.check_requirements():
            print("\n❌ Please fix missing files before deployment")
            return
        
        # Create necessary config files
        self.create_streamlit_secrets()
        
        while True:
            choice = self.show_menu()
            
            if choice == '0':
                print("\n👋 Happy deploying!")
                break
            elif choice == '1':
                self.deploy_streamlit_cloud()
            elif choice == '2':
                self.deploy_docker()
            elif choice == '3':
                self.deploy_heroku()
            elif choice == '4':
                self.deploy_railway()
            elif choice == '5':
                self.deploy_streamlit_cloud()
                self.deploy_docker()
                self.deploy_heroku()
                self.deploy_railway()
            else:
                print("❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    deployer = ServerDeployer()
    deployer.run()