# 🤖🍳 AI Chef Bot - HuggingFace Powered

Intelligent AI cooking assistant powered by HuggingFace models with voice chat and photo analysis.

## ✨ Features
- 🤖 **AI Conversations** - DialoGPT-medium powered recipe discussions
- 📸 **Smart Vision** - BLIP model analyzes food photos
- 🎤 **Voice Chat** - Talk to the AI with your voice
- 📱 **Mobile Responsive** - Works perfectly on phones and tablets
- 🎨 **Beautiful Design** - Clean, modern interface

## 🤗 HuggingFace Models
- **Text Generation:** `microsoft/DialoGPT-medium` (345MB)
- **Image Analysis:** `Salesforce/blip-image-captioning-base` (990MB)
- **Voice:** Google Speech Recognition + Windows TTS

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirement.txt
```

### 2. Get HuggingFace Token (Required for AI)
- Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create free token
- Add to `.env` file:
```env
HUGGINGFACE_API_KEY=your_token_here
```

### 3. Run the AI Chef Bot
```bash
# Run the AI-powered chef bot
streamlit run chef_bot_huggingface.py

# Or use the launcher
python run_chef_bot.py
```

## 📁 Project Files
- `chef_bot_huggingface.py` - Main AI-powered application
- `run_chef_bot.py` - Easy launcher script
- `requirement.txt` - Dependencies
- `.env` - Environment variables (create this file)
- `README.md` - This documentation

## 🌐 Deploy to Streamlit Cloud
1. Push to GitHub (don't include .env file)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Set main file: `chef_bot_huggingface.py`
5. Add HuggingFace token in Streamlit Cloud secrets
6. Deploy in 1 click!

## 🔧 Configuration

### With HuggingFace Token:
- ✅ AI-generated recipe responses
- ✅ Smart image analysis
- ✅ Natural conversations
- ✅ High-quality cooking advice

### Without Token (Fallback):
- ✅ Hardcoded recipe responses
- ✅ Basic image analysis
- ✅ All features still work
- ⚠️ Less intelligent responses

## 🎯 Try These AI Prompts
- "Create a unique pasta recipe with what I have"
- "Analyze this photo and suggest creative recipes"
- "I'm vegetarian, what's a protein-rich dinner?"
- "Quick breakfast for busy mornings"
- Upload photos of your fridge contents!

## 🤖 AI Capabilities
- **Natural Language Understanding** - Understands complex cooking questions
- **Recipe Generation** - Creates custom recipes based on ingredients
- **Image Recognition** - Identifies food items in photos
- **Conversational Memory** - Remembers context within chat session
- **Cooking Expertise** - Trained on cooking and recipe data

---
**🤖🍳 Happy AI Cooking!** Powered by HuggingFace • Made with ❤️ and Streamlit