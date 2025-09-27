# This is a copy of chef_bot_huggingface.py for HuggingFace Spaces deployment
# HuggingFace Spaces expects the main file to be named 'app.py'

import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
from PIL import Image
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="🍳 Chef Bot - HuggingFace",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Beautiful CSS (same as before)
st.markdown("""
<style>
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Beautiful gradient background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Custom chat message styling */
.user-message {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    margin: 0.5rem 0;
    margin-left: 20%;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    animation: slideInRight 0.3s ease-out;
}

.bot-message {
    background: white;
    color: #1f2937;
    padding: 1rem 1.5rem;
    border-radius: 20px;
    margin: 0.5rem 0;
    margin-right: 20%;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #10b981;
    animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

/* Welcome card styling */
.welcome-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 3rem 2rem;
    margin: 2rem 0;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-card {
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    transition: transform 0.2s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    margin: 0.5rem;
}

.feature-card:hover {
    transform: translateY(-5px);
}

/* Input container */
.input-container {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Sidebar styling */
.sidebar-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Mobile responsive */
@media (max-width: 768px) {
    .user-message, .bot-message {
        margin-left: 5%;
        margin-right: 5%;
    }
    
    .welcome-card {
        padding: 2rem 1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# HuggingFace AI Bot Class
class HuggingFaceChefBot:
    def __init__(self):
        # Try to get API key from multiple sources
        self.hf_token = (
            os.getenv("HUGGINGFACE_API_KEY") or 
            os.getenv("HF_TOKEN") or 
            st.secrets.get("HUGGINGFACE_API_KEY", "") if hasattr(st, 'secrets') else ""
        )
        self.headers = {"Authorization": f"Bearer {self.hf_token}"} if self.hf_token else {}
        
        # Model endpoints
        self.chat_model = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.image_model = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
        
        # TTS setup (may not work on all servers)
        self.tts_engine = None
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 170)
            self.tts_engine.setProperty('volume', 0.9)
        except:
            pass
    
    def speak(self, text):
        if not self.tts_engine:
            return
        try:
            # Clean text for speech
            clean_text = text.replace('🍳', '').replace('🍝', '').replace('🐔', '')
            clean_text = clean_text.replace('🥗', '').replace('⚡', '').replace('🍰', '')
            clean_text = clean_text.replace('*', '').replace('#', '')
            
            if len(clean_text) > 200:
                clean_text = clean_text[:200] + "..."
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
        except:
            pass
    
    def listen(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=8, phrase_time_limit=12)
            return r.recognize_google(audio)
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand"
        except:
            return "Microphone error"
    
    def get_cooking_response(self, user_input):
        """Get AI response for cooking questions"""
        try:
            # Create cooking-focused prompt
            cooking_prompt = f"""You are a helpful cooking assistant. User asks: {user_input}
            
            Provide a helpful, friendly response about cooking, recipes, or food. Keep it concise and practical."""
            
            payload = {
                "inputs": cooking_prompt,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "do_sample": True,
                    "pad_token_id": 50256
                }
            }
            
            if not self.hf_token:
                # Fallback responses when no API key
                return self.get_fallback_response(user_input)
            
            response = requests.post(self.chat_model, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract only the response part
                    if 'Provide a helpful' in generated_text:
                        response_text = generated_text.split('Provide a helpful')[0].strip()
                    else:
                        response_text = generated_text.replace(cooking_prompt, '').strip()
                    
                    if response_text:
                        return f"🍳 {response_text}"
            
            return self.get_fallback_response(user_input)
            
        except Exception as e:
            return self.get_fallback_response(user_input)
    
    def get_fallback_response(self, user_input):
        """Fallback responses when AI is not available"""
        user_lower = user_input.lower()
        
        fallback_responses = {
            'pasta': "🍝 **Quick Pasta Recipe:**\n\n1. Boil pasta in salted water\n2. Sauté garlic in olive oil\n3. Add tomatoes and fresh basil\n4. Toss with pasta and parmesan\n\n*Ready in 15 minutes!*",
            'chicken': "🐔 **Simple Chicken Dish:**\n\n1. Season chicken breast with salt and pepper\n2. Pan-fry until golden brown\n3. Serve with steamed vegetables\n4. Add rice or mashed potatoes\n\n*Healthy and delicious!*",
            'salad': "🥗 **Fresh Salad Ideas:**\n\n• Mixed greens with cherry tomatoes\n• Cucumber and red onion\n• Your favorite dressing\n• Add protein like grilled chicken\n\n*Light and nutritious!*",
            'quick': "⚡ **Quick Meal Ideas:**\n\n• Scrambled eggs with toast\n• Avocado toast with tomatoes\n• Simple sandwich with fresh ingredients\n• Instant oatmeal with fruits\n\n*Ready in 5 minutes!*",
            'dessert': "🍰 **Easy Desserts:**\n\n• Greek yogurt with honey and berries\n• Chocolate mug cake (microwave 2 min)\n• Fresh fruit with whipped cream\n• Ice cream with nuts\n\n*Sweet and simple!*",
            'breakfast': "🌅 **Breakfast Ideas:**\n\n• Oatmeal with fresh fruits\n• Eggs any style with toast\n• Smoothie bowl with granola\n• Pancakes with maple syrup\n\n*Start your day right!*"
        }
        
        for key, response in fallback_responses.items():
            if key in user_lower:
                return response
        
        return "🍳 **I'm here to help you cook!**\n\nTry asking me about:\n• Pasta recipes\n• Chicken dishes\n• Fresh salads\n• Quick meals\n• Easy desserts\n• Breakfast ideas\n\n*What sounds good to you?*"
    
    def analyze_image(self, image):
        """Analyze food image using HuggingFace BLIP model"""
        try:
            if not self.hf_token:
                return "📸 **Great photo!** I can see your ingredients. Here are some ideas:\n\n• **Stir-fry** - Quick and healthy\n• **Pasta dish** - Always delicious\n• **Fresh salad** - Light and nutritious\n• **Soup** - Warm and comforting\n\n*What type of dish are you in the mood for?*"
            
            # Convert image to bytes
            import io
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            response = requests.post(
                self.image_model,
                headers=self.headers,
                data=img_byte_arr,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    caption = result[0].get('generated_text', '')
                    return f"📸 **I can see:** {caption}\n\n**Recipe suggestions:**\n• Use these ingredients in a stir-fry\n• Make a fresh salad or soup\n• Try grilling or roasting them\n• Perfect for a pasta dish!\n\n*What cooking style do you prefer?*"
            
            return "📸 **Great photo!** I can see your delicious ingredients. Try making a stir-fry, pasta dish, or fresh salad with what you have!"
            
        except Exception as e:
            return "📸 **Nice photo!** Here are some general recipe ideas:\n\n• **Stir-fry** - Quick and versatile\n• **Soup** - Warm and comforting\n• **Salad** - Fresh and healthy\n• **Pasta** - Always satisfying"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'hf_bot' not in st.session_state:
    st.session_state.hf_bot = HuggingFaceChefBot()
if 'voice_mode' not in st.session_state:
    st.session_state.voice_mode = False

def add_message(user_msg, bot_msg):
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.messages.append({"role": "bot", "content": bot_msg})
    
    if st.session_state.voice_mode:
        threading.Thread(target=st.session_state.hf_bot.speak, args=(bot_msg,)).start()

# Main Layout
col1, col2 = st.columns([3, 1])

with col1:
    # Chat Area
    if st.session_state.messages:
        st.markdown("### 💬 Chat with AI Chef Bot")
        
        # Display messages
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f'<div class="user-message">👤 {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-message">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        # Welcome Screen
        st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
        
        # Large cooking emoji
        st.markdown("<div style='text-align: center; font-size: 4rem; margin-bottom: 1rem;'>🤖🍳</div>", unsafe_allow_html=True)
        
        # Title and subtitle
        st.markdown("# AI Chef Bot - HuggingFace Powered!")
        st.markdown("### Intelligent cooking assistant with DialoGPT & BLIP models")
        
        # Feature cards using Streamlit columns
        col_chat, col_voice, col_photo = st.columns(3)
        
        with col_chat:
            st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🤖</div>
                <div style="font-weight: 600; color: #374151;">AI Chat</div>
                <div style="color: #6b7280; font-size: 0.9rem;">DialoGPT-medium powered</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_voice:
            st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎤</div>
                <div style="font-weight: 600; color: #374151;">Voice</div>
                <div style="color: #6b7280; font-size: 0.9rem;">Talk to AI assistant</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_photo:
            st.markdown("""
            <div class="feature-card">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📸</div>
                <div style="font-weight: 600; color: #374151;">Vision</div>
                <div style="color: #6b7280; font-size: 0.9rem;">BLIP image analysis</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Input Area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # API Key status
    if st.session_state.hf_bot.hf_token:
        st.success("🤗 HuggingFace API connected - AI responses enabled!")
    else:
        st.warning("⚠️ No HuggingFace API key - Using fallback responses. Add HUGGINGFACE_API_KEY to secrets for AI features.")
    
    # Tabs for input methods
    tab1, tab2, tab3 = st.tabs(["💬 **AI Chat**", "🎤 **Voice**", "📸 **Vision**"])
    
    with tab1:
        st.markdown("#### Ask the AI anything about cooking")
        user_input = st.text_area("Chat with AI Chef...", placeholder="What would you like to cook today?", height=100)
        
        col_send, col_voice, col_clear = st.columns([2, 1, 1])
        
        with col_send:
            if st.button("🤖 **Ask AI**", type="primary"):
                if user_input.strip():
                    with st.spinner("🤖 AI is thinking..."):
                        response = st.session_state.hf_bot.get_cooking_response(user_input)
                        add_message(user_input, response)
                        st.rerun()
        
        with col_voice:
            voice_mode = st.toggle("🔊 **Voice**", value=st.session_state.voice_mode)
            st.session_state.voice_mode = voice_mode
        
        with col_clear:
            if st.button("🗑️ **Clear**"):
                st.session_state.messages = []
                st.rerun()
    
    with tab2:
        st.markdown("#### Voice Input with AI")
        st.info("🎤 Click the button below and speak your cooking question!")
        
        if st.button("🎤 **Record & Ask AI**", type="primary"):
            with st.spinner("🎧 Listening... Please speak now!"):
                voice_input = st.session_state.hf_bot.listen()
                
                if "error" not in voice_input.lower() and "no speech" not in voice_input.lower():
                    st.success(f"✅ You said: **{voice_input}**")
                    with st.spinner("🤖 AI is processing your voice..."):
                        response = st.session_state.hf_bot.get_cooking_response(voice_input)
                        add_message(voice_input, response)
                        st.rerun()
                else:
                    st.error(f"❌ {voice_input}")
    
    with tab3:
        st.markdown("#### AI Vision Analysis")
        st.info("📸 Upload a food photo for AI-powered analysis!")
        
        uploaded_file = st.file_uploader(
            "Choose a food photo...",
            type=['png', 'jpg', 'jpeg'],
            help="AI will analyze your photo using BLIP model!"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 Your photo for AI analysis", use_column_width=True)
            
            if st.button("🤖 **AI Analyze Photo**", type="primary"):
                with st.spinner("🤖 AI is analyzing your photo..."):
                    analysis = st.session_state.hf_bot.analyze_image(image)
                    add_message("📸 Uploaded photo for AI analysis", analysis)
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Model Info Sidebar
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🤗 **AI Models**")
    st.markdown("""
    **Text Generation:**
    • DialoGPT-medium (345MB)
    • Conversational AI responses
    
    **Image Analysis:**
    • BLIP-image-captioning
    • Food photo understanding
    
    **Voice Features:**
    • Google Speech Recognition
    • Windows TTS Engine
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Recipes Sidebar
    st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 **Quick AI Recipes**")
    
    quick_recipes = [
        ("🍝 AI Pasta", "Give me a creative pasta recipe"),
        ("🐔 AI Chicken", "Suggest an innovative chicken dish"),
        ("🥗 AI Salad", "Create a unique salad recipe"),
        ("⚡ AI Quick", "What's a quick meal I can make?"),
        ("🍰 AI Dessert", "Suggest a creative dessert"),
        ("🌅 AI Breakfast", "Give me breakfast inspiration")
    ]
    
    for name, prompt in quick_recipes:
        if st.button(name, key=f"ai_{prompt}", use_container_width=True):
            with st.spinner("🤖 AI is creating recipe..."):
                response = st.session_state.hf_bot.get_cooking_response(prompt)
                add_message(prompt, response)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.8); padding: 1rem;">
    <strong>🤖🍳 AI Chef Bot</strong> • BY NAZANIN • Deployed on Free Server
</div>
""", unsafe_allow_html=True)