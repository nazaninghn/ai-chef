import streamlit as st
from PIL import Image
import speech_recognition as sr
import pyttsx3
import threading
import requests
import json
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Custom CSS for better design
def load_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: fadeIn 0.5s;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 2rem;
    }
    
    .quick-button {
        background: linear-gradient(45deg, #FF9A8B, #A8E6CF);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        margin: 0.2rem;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .quick-button:hover {
        transform: scale(1.05);
    }
    
    .recipe-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #FF6B6B;
    }
    
    .ingredient-tag {
        background: #E8F5E8;
        color: #2E7D32;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        display: inline-block;
        font-size: 0.9rem;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

class FastRecipeBot:
    def __init__(self):
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        self.recipe_database = self.load_recipe_database()
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        try:
            self.tts_engine.setProperty('rate', 180)
            self.tts_engine.setProperty('volume', 0.9)
        except:
            pass
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            clean_text = text.replace('*', '').replace('#', '').replace('```', '')
            if len(clean_text) > 300:
                clean_text = clean_text[:300] + "..."
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
        except Exception as e:
            st.error(f"Speech error: {e}")
    
    def listen(self):
        """Convert speech to text"""
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=8, phrase_time_limit=10)
            
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "⏰ Timeout - please try again"
        except sr.UnknownValueError:
            return "🤔 Couldn't understand - please speak clearly"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def load_recipe_database(self):
        """Load a fast, local recipe database"""
        return {
            'chicken': {
                'recipes': [
                    {
                        'name': '🍗 Quick Chicken Stir-Fry',
                        'time': '15 mins',
                        'ingredients': ['chicken breast', 'vegetables', 'soy sauce', 'garlic'],
                        'steps': ['Cut chicken into strips', 'Heat oil in pan', 'Cook chicken 5 mins', 'Add vegetables', 'Stir-fry 5 mins', 'Add soy sauce']
                    },
                    {
                        'name': '🍖 Grilled Chicken',
                        'time': '20 mins',
                        'ingredients': ['chicken breast', 'olive oil', 'herbs', 'salt', 'pepper'],
                        'steps': ['Season chicken', 'Heat grill', 'Cook 8 mins each side', 'Rest 5 mins', 'Serve hot']
                    }
                ]
            },
            'pasta': {
                'recipes': [
                    {
                        'name': '🍝 Garlic Butter Pasta',
                        'time': '12 mins',
                        'ingredients': ['pasta', 'garlic', 'butter', 'parmesan', 'parsley'],
                        'steps': ['Boil pasta', 'Sauté garlic in butter', 'Toss pasta with garlic butter', 'Add parmesan', 'Garnish with parsley']
                    },
                    {
                        'name': '🍅 Tomato Basil Pasta',
                        'time': '15 mins',
                        'ingredients': ['pasta', 'tomatoes', 'basil', 'garlic', 'olive oil'],
                        'steps': ['Cook pasta', 'Sauté garlic', 'Add tomatoes', 'Simmer 5 mins', 'Add basil and pasta']
                    }
                ]
            },
            'vegetarian': {
                'recipes': [
                    {
                        'name': '🥗 Rainbow Salad',
                        'time': '10 mins',
                        'ingredients': ['mixed greens', 'tomatoes', 'cucumber', 'carrots', 'dressing'],
                        'steps': ['Wash vegetables', 'Chop all ingredients', 'Mix in bowl', 'Add dressing', 'Toss and serve']
                    },
                    {
                        'name': '🍳 Veggie Scramble',
                        'time': '8 mins',
                        'ingredients': ['eggs', 'bell peppers', 'onions', 'cheese', 'herbs'],
                        'steps': ['Beat eggs', 'Sauté vegetables', 'Add eggs', 'Scramble gently', 'Add cheese']
                    }
                ]
            },
            'quick': {
                'recipes': [
                    {
                        'name': '🥪 Grilled Cheese',
                        'time': '5 mins',
                        'ingredients': ['bread', 'cheese', 'butter'],
                        'steps': ['Butter bread', 'Add cheese', 'Grill until golden', 'Flip and repeat', 'Serve hot']
                    },
                    {
                        'name': '🍌 Smoothie Bowl',
                        'time': '3 mins',
                        'ingredients': ['banana', 'berries', 'yogurt', 'granola', 'honey'],
                        'steps': ['Blend banana and berries', 'Pour into bowl', 'Top with granola', 'Drizzle honey', 'Enjoy!']
                    }
                ]
            }
        }
    
    def analyze_image_fast(self, image):
        """Fast image analysis with recipe suggestions"""
        try:
            # Get image dimensions and basic info
            width, height = image.size
            format_type = image.format or "Unknown"
            
            # Simple color analysis to guess food types
            import numpy as np
            img_array = np.array(image.resize((100, 100)))  # Small size for speed
            
            # Calculate average colors
            avg_colors = np.mean(img_array, axis=(0, 1))
            
            # Simple food detection based on colors
            detected_foods = []
            
            # Red/orange tones - tomatoes, peppers, meat
            if avg_colors[0] > 120 and avg_colors[1] < 100:
                detected_foods.extend(['tomatoes', 'red peppers', 'meat'])
            
            # Green tones - vegetables, herbs
            if avg_colors[1] > avg_colors[0] and avg_colors[1] > avg_colors[2]:
                detected_foods.extend(['lettuce', 'herbs', 'vegetables'])
            
            # Yellow/orange - cheese, eggs, citrus
            if avg_colors[0] > 150 and avg_colors[1] > 150 and avg_colors[2] < 100:
                detected_foods.extend(['cheese', 'eggs', 'citrus'])
            
            # Brown tones - bread, meat, chocolate
            if all(c > 80 and c < 150 for c in avg_colors):
                detected_foods.extend(['bread', 'chicken', 'beef'])
            
            # Generate response based on detected foods
            if detected_foods:
                # Remove duplicates
                unique_foods = list(set(detected_foods))
                
                response = f"📸 **Great photo! I can see some delicious ingredients!**\n\n"
                response += f"🔍 **I detect:** {', '.join(unique_foods[:4])}\n\n"
                
                # Get recipes based on detected ingredients
                recipe_suggestions = []
                for food in unique_foods[:2]:  # Limit for speed
                    for category, data in self.recipe_database.items():
                        for recipe in data['recipes']:
                            if any(food.lower() in ingredient.lower() for ingredient in recipe['ingredients']):
                                if recipe not in recipe_suggestions:
                                    recipe_suggestions.append(recipe)
                                    break
                        if len(recipe_suggestions) >= 2:
                            break
                
                if recipe_suggestions:
                    response += "🍳 **Perfect recipes for your ingredients:**\n\n"
                    for recipe in recipe_suggestions[:2]:
                        response += f"### {recipe['name']}\n"
                        response += f"⏱️ **Time:** {recipe['time']}\n\n"
                        response += "**You'll need:**\n"
                        for ingredient in recipe['ingredients'][:4]:
                            response += f"• {ingredient}\n"
                        response += f"\n**Quick steps:**\n"
                        for i, step in enumerate(recipe['steps'][:3], 1):
                            response += f"{i}. {step}\n"
                        response += "\n---\n\n"
                else:
                    response += self.get_generic_photo_response()
            else:
                response = self.get_generic_photo_response()
            
            return response
            
        except Exception as e:
            return f"📸 I can see your photo! While I can't analyze it in detail, I'd love to help you cook something amazing!\n\n{self.get_generic_photo_response()}"
    
    def get_generic_photo_response(self):
        """Generic helpful response for photos"""
        return """💡 **Here's what I can help with:**

🍳 **Tell me what you see and I'll suggest recipes!**

**For example, say:**
• "I see chicken and vegetables"
• "There's pasta and tomatoes"  
• "I have eggs and cheese"

🎯 **Or try these popular combos:**

### 🍗 **Chicken + Rice**
Perfect for stir-fries and one-pot meals!

### 🍝 **Pasta + Tomatoes**
Classic Italian combinations!

### 🥚 **Eggs + Vegetables**
Great for omelets and scrambles!

Just describe what ingredients you have, and I'll give you amazing recipes! 🌟"""

    def get_fast_response(self, user_input):
        """Generate fast responses using local database"""
        user_lower = user_input.lower()
        
        # Find matching category
        for category, data in self.recipe_database.items():
            if category in user_lower or any(ingredient in user_lower for recipe in data['recipes'] for ingredient in recipe['ingredients']):
                recipes = data['recipes'][:2]  # Limit to 2 recipes for speed
                
                response = f"🍳 **Great choice! Here are some {category} recipes:**\n\n"
                
                for recipe in recipes:
                    response += f"### {recipe['name']}\n"
                    response += f"⏱️ **Time:** {recipe['time']}\n\n"
                    response += f"**Ingredients:**\n"
                    for ingredient in recipe['ingredients']:
                        response += f"• {ingredient}\n"
                    response += f"\n**Steps:**\n"
                    for i, step in enumerate(recipe['steps'], 1):
                        response += f"{i}. {step}\n"
                    response += "\n---\n\n"
                
                return response
        
        # Default quick responses
        if any(word in user_lower for word in ['quick', 'fast', 'easy']):
            return """⚡ **Super Quick Recipes (Under 10 minutes):**

### 🥪 Perfect Grilled Cheese
⏱️ **5 minutes**
• Butter bread slices
• Add your favorite cheese
• Grill until golden and crispy

### 🍌 Energy Smoothie
⏱️ **3 minutes**  
• Blend banana + berries + yogurt
• Top with granola and honey
• Perfect breakfast or snack!

### 🍳 Scrambled Eggs
⏱️ **4 minutes**
• Beat 2-3 eggs with salt
• Cook in buttered pan, stirring gently
• Add cheese in last 30 seconds"""

        elif any(word in user_lower for word in ['healthy', 'diet', 'nutrition']):
            return """🥗 **Healthy & Nutritious Options:**

### 🌈 Rainbow Buddha Bowl
⏱️ **15 minutes**
• Quinoa + roasted vegetables
• Avocado + chickpeas
• Tahini dressing

### 🐟 Baked Salmon
⏱️ **20 minutes**
• Season salmon with herbs
• Bake at 400°F for 12-15 mins
• Serve with steamed broccoli

### 🥑 Avocado Toast Plus
⏱️ **5 minutes**
• Toast whole grain bread
• Mash avocado with lime
• Top with tomato and seeds"""

        else:
            return """👋 **Hi! I'm your fast recipe assistant!**

🎯 **Try asking me:**
• "Quick dinner ideas"
• "Chicken recipes"
• "Vegetarian meals"
• "Healthy options"
• "Pasta dishes"

💡 **Or use the quick buttons below for instant recipes!**

I'll give you fast, practical recipes with simple ingredients and easy steps! 🍳✨"""

def main():
    st.set_page_config(
        page_title="⚡ Fast Recipe Assistant",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Fast Recipe Assistant</h1>
        <p>Lightning-fast recipes with beautiful design!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize the bot
    if 'bot' not in st.session_state:
        st.session_state.bot = FastRecipeBot()
    
    # Initialize conversation history
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
    
    # Initialize voice mode
    if 'voice_mode' not in st.session_state:
        st.session_state.voice_mode = False
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ **Controls**")
        
        # Voice mode toggle
        voice_mode = st.checkbox("🎤 Voice Mode", value=st.session_state.voice_mode)
        st.session_state.voice_mode = voice_mode
        
        if voice_mode:
            st.success("🎤 Voice mode ON!")
        
        # Clear conversation
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.conversation = []
            st.rerun()
        
        st.markdown("---")
        
        # Quick recipe categories
        st.markdown("### 🚀 **Quick Recipes**")
        
        quick_categories = [
            ("⚡ Super Fast", "quick recipes under 5 minutes"),
            ("🍗 Chicken", "chicken recipes"),
            ("🍝 Pasta", "pasta dishes"),
            ("🥗 Healthy", "healthy meal options"),
            ("🥪 Snacks", "quick snack ideas")
        ]
        
        for emoji_title, prompt in quick_categories:
            if st.button(emoji_title, use_container_width=True):
                response = st.session_state.bot.get_fast_response(prompt)
                st.session_state.conversation.append({
                    'user': prompt,
                    'bot': response
                })
                st.rerun()
        
        st.markdown("---")
        
        # Image upload tip
        st.markdown("### 📸 **Photo Analysis**")
        st.info("💡 Upload photos of your fridge, ingredients, or meals for instant recipe suggestions!")
        
        st.markdown("---")
        st.markdown("### 💡 **Features**")
        st.markdown("""
        ✅ **Lightning Fast** - Instant responses
        ✅ **Beautiful Design** - Modern UI
        ✅ **Voice Support** - Talk to me!
        ✅ **Image Upload** - Analyze food photos
        ✅ **No API Keys** - Completely free
        ✅ **Local Database** - Works offline
        """)
    
    # Main chat area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💬 **Chat with Recipe Bot**")
        
        # Display conversation history with custom styling
        for i, msg in enumerate(st.session_state.conversation):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {msg['user']}
            </div>
            """, unsafe_allow_html=True)
            
            # Bot response
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 Chef Bot:</strong>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(msg['bot'])
            
            # Speak button
            if st.button(f"🔊 Speak", key=f"speak_{i}"):
                threading.Thread(
                    target=st.session_state.bot.speak, 
                    args=(msg['bot'],)
                ).start()
        
        # Input methods
        st.markdown("---")
        input_method = st.radio("**Choose input method:**", ["💬 Type", "🎤 Voice", "📸 Image"], horizontal=True)
        
        if input_method == "💬 Type":
            user_input = st.chat_input("Ask me about recipes, ingredients, or cooking tips...")
            
            if user_input:
                # Add to conversation
                with st.spinner("🍳 Cooking up a response..."):
                    bot_response = st.session_state.bot.get_fast_response(user_input)
                    
                    st.session_state.conversation.append({
                        'user': user_input,
                        'bot': bot_response
                    })
                    
                    # Auto-speak in voice mode
                    if st.session_state.voice_mode:
                        threading.Thread(
                            target=st.session_state.bot.speak, 
                            args=(bot_response,)
                        ).start()
                    
                    st.rerun()
        
        elif input_method == "🎤 Voice":
            col_voice1, col_voice2 = st.columns([1, 1])
            
            with col_voice1:
                if st.button("🎤 **Start Recording**", type="primary", use_container_width=True):
                    with st.spinner("🎤 Listening..."):
                        voice_input = st.session_state.bot.listen()
                        
                        if not any(word in voice_input.lower() for word in ['timeout', 'error', 'couldn\'t']):
                            st.success(f"✅ You said: '{voice_input}'")
                            
                            with st.spinner("🍳 Preparing response..."):
                                bot_response = st.session_state.bot.get_fast_response(voice_input)
                                
                                st.session_state.conversation.append({
                                    'user': voice_input,
                                    'bot': bot_response
                                })
                                
                                # Auto-speak response
                                threading.Thread(
                                    target=st.session_state.bot.speak, 
                                    args=(bot_response,)
                                ).start()
                                
                                st.rerun()
                        else:
                            st.error(voice_input)
            
            with col_voice2:
                st.info("💡 **Voice Tips:**\n- Speak clearly\n- Keep it under 10 seconds\n- Try: 'Quick chicken recipe'")
        
        elif input_method == "📸 Image":
            st.markdown("### 📸 **Upload Food Photo**")
            
            uploaded_file = st.file_uploader(
                "Upload a photo of your ingredients or food:",
                type=['png', 'jpg', 'jpeg'],
                help="I'll analyze your photo and suggest recipes!"
            )
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                
                # Display image with custom styling
                st.markdown("""
                <div class="recipe-card">
                    <h4>📸 Your Uploaded Image</h4>
                </div>
                """, unsafe_allow_html=True)
                
                st.image(image, caption="Your food photo", use_column_width=True)
                
                col_img1, col_img2 = st.columns([1, 1])
                
                with col_img1:
                    if st.button("🔍 **Analyze Photo**", type="primary", use_container_width=True):
                        with st.spinner("🔍 Analyzing your delicious photo..."):
                            analysis = st.session_state.bot.analyze_image_fast(image)
                            
                            st.session_state.conversation.append({
                                'user': "[Uploaded a food photo]",
                                'bot': analysis
                            })
                            
                            # Auto-speak in voice mode
                            if st.session_state.voice_mode:
                                threading.Thread(
                                    target=st.session_state.bot.speak, 
                                    args=(analysis,)
                                ).start()
                            
                            st.rerun()
                
                with col_img2:
                    st.info("💡 **Photo Tips:**\n- Good lighting works best\n- Show ingredients clearly\n- Multiple ingredients = better recipes!")
    
    with col2:
        st.markdown("### 🎯 **Popular Recipes**")
        
        # Featured recipes with beautiful cards
        featured_recipes = [
            ("🍝 Garlic Pasta", "pasta recipes"),
            ("🍗 Chicken Stir-Fry", "chicken stir fry"),
            ("🥗 Fresh Salad", "healthy salad"),
            ("🍳 Quick Eggs", "egg recipes"),
            ("🥪 Grilled Cheese", "grilled cheese")
        ]
        
        for recipe_name, prompt in featured_recipes:
            if st.button(recipe_name, use_container_width=True):
                response = st.session_state.bot.get_fast_response(prompt)
                st.session_state.conversation.append({
                    'user': f"Tell me about {recipe_name}",
                    'bot': response
                })
                st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚡ **Why So Fast?**")
        st.markdown("""
        🚀 **Local Database** - No API calls
        💾 **Cached Responses** - Instant results  
        🎨 **Optimized UI** - Smooth animations
        ⚡ **Smart Matching** - Quick recipe finding
        """)

if __name__ == "__main__":
    main()