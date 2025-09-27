# 🔑 API Key Setup Guide

## 🚨 **IMPORTANT: You need to get your FREE Gemini API key first!**

### **Step 1: Get Your Free API Key**

1. **Go to Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Create API Key"**
4. **Copy the generated key** (starts with "AIza...")

### **Step 2: Add Your API Key**

1. **Open the `.env` file** in your project
2. **Replace** `your_actual_api_key_here` with your real API key:

```
GEMINI_API_KEY=AIzaSyYourRealApiKeyHere123456789
```

**Example:**
```
GEMINI_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz
```

### **Step 3: Test Your Setup**

Run the demo to test:
```cmd
python chatbot_demo.py
```

If it works, run the full chatbot:
```cmd
python run_chatbot.py
```

## ❌ **Common Issues:**

### **"No API_KEY found" Error:**
- Make sure your `.env` file has the correct API key
- No spaces around the `=` sign
- API key should start with `AIza`

### **"Invalid API Key" Error:**
- Double-check you copied the full key from Google AI Studio
- Make sure the key is active (not revoked)

### **"Quota Exceeded" Error:**
- Gemini has generous free limits, but if exceeded, wait or create a new key

## 🆓 **Free Tier Limits:**
- **15 requests per minute**
- **1,500 requests per day**
- **No credit card required**

## 🔒 **Security Note:**
- Never share your API key publicly
- Don't commit the `.env` file to version control
- Keep your key private

---

**Need help?** The API key should look like: `AIzaSyC1234567890abcdefghijklmnopqrstuvwxyz`