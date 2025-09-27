"""
Launch the AI Chef Bot - HuggingFace Powered
Intelligent cooking assistant with DialoGPT & BLIP models
"""

import subprocess
import sys
import os

def main():
    print("🤖🍳 Starting AI Chef Bot...")
    print("🤗 Powered by HuggingFace models")
    print("💬 DialoGPT-medium for conversations")
    print("📸 BLIP for image analysis")
    print("🎤 Voice chat enabled")
    print("📱 Mobile responsive")
    print("\n" + "="*50)
    print("🌐 Opening in your browser...")
    print("🔗 URL: http://localhost:8501")
    print("="*50 + "\n")
    
    try:
        # Run the HuggingFace AI chef bot
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "chef_bot_huggingface.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Thanks for using AI Chef Bot!")
    except Exception as e:
        print(f"❌ Error starting the app: {e}")
        print("💡 Make sure you have streamlit installed: pip install streamlit")
        print("💡 Get free HuggingFace token at: https://huggingface.co/settings/tokens")

if __name__ == "__main__":
    main()