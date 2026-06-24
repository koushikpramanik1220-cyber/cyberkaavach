import streamlit as st
import os
import google.generativeai as genai

# --- STREAMLIT CONFIGURATION ---
st.set_page_config(page_title="CyberKavach AI - Cyber Helpdesk", page_icon="🛡️", layout="wide")

# --- SECURE AI CONFIGURATION ---
# Fetches key from st.secrets (Streamlit Cloud) or local environment variables safely
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.sidebar.warning("⚠️ API Key not detected. Please configure GEMINI_API_KEY to activate AI features.")

def analyze_with_ai(prompt_text):
    """Function to analyze text or links using Gemini AI"""
    if not api_key:
        return "System Misconfiguration: Missing Gemini API Key. Please run locally with environment variables or configure Streamlit Secrets."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return "Sorry, the AI helper is currently offline. Please stay cautious and do not share any sensitive data."

# --- UI DESIGN ---
st.title("🛡️ CyberKavach AI (Cyber-Suraksha AI Helpdesk)")
st.subheader("An Easy-to-Use AI Cyber Protector for Common & Rural People")
st.write("---")

# Sidebar for Emergency Help and Tips
with st.sidebar:
    st.header("🚨 Emergency Assistance")
    st.error("📞 National Cyber Helpline: **1930**")
    st.info("🌐 Official Portal: [cybercrime.gov.in](https://cybercrime.gov.in)")
    st.write("---")
    st.markdown("""
    **💡 Quick Safety Tips:**
    * Never share your OTP (One-Time Password) or banking passwords with anyone.
    * Do not trust messages claiming you won a lottery or that your bank account is blocked.
    * Always check suspicious links here before clicking them.
    """)

# Creating Tabs for the 3 core features
tab1, tab2, tab3 = st.tabs([
    "🔗 Scam Link Checker", 
    "💬 Fraud SMS/Email Analyzer", 
    "📋 Cyber Complaint Guide"
])

# --- TAB 1: SCAM LINK CHECKER ---
with tab1:
    st.header("🔍 Verify Suspicious Links (URLs)")
    st.write("Received a suspicious link on WhatsApp or SMS? Let the AI check if it is safe or a trap.")
    
    user_url = st.text_input("Paste the URL/Link here:", placeholder="https://example.com/free-gifts")
    
    if st.button("Verify Link", key="btn_link"):
        if user_url:
            with st.spinner("AI is analyzing the security of the link..."):
                prompt = f"""
                Analyze this URL: {user_url}. 
                Is it a potential phishing scam, fake lottery, malware, or malicious website? 
                Provide a clear summary in simple English. Explain if it looks safe or dangerous, 
                and give a direct warning tailored for common/rural people. Keep it simple and easy to understand.
                """
                ai_result = analyze_with_ai(prompt)
                st.warning("⚠️ AI Analysis Result:")
                st.write(ai_result)
        else:
            st.info("Please enter a link to analyze.")

# --- TAB 2: FRAUD SMS/EMAIL ANALYZER ---
with tab2:
    st.header("💬 Analyze Suspicious Messages & Emails")
    st.write("Paste suspicious texts regarding bank blocks, fake jobs, or unexpected prize money here.")
    
    user_msg = st.text_area("Paste the message text here:", placeholder="Your bank account is blocked, click here to update...", height=150)
    
    if st.button("Analyze Message", key="btn_msg"):
        if user_msg:
            with st.spinner("AI is reading through the message patterns..."):
                prompt = f"""
                Analyze the following message for fraud, phishing, or scams:
                "{user_msg}"
                
                Respond in simple English. Break it down into:
                1. Is it a fraud? (Yes or No)
                2. Why is it a fraud? (Explain the red flags simply)
                3. What should the user do next? (Actionable steps like ignoring, deleting, blocking)
                Keep the tone extremely helpful, protective, and friendly for elderly or non-technical people.
                """
                ai_result = analyze_with_ai(prompt)
                st.success("🤖 CyberKavach AI Advice:")
                st.write(ai_result)
        else:
            st.info("Please paste the message text to analyze.")

# --- TAB 3: CYBER COMPLAINT GUIDE ---
with tab3:
    st.header("📋 One-Click Cyber Complaint Guide")
    st.write("Have you or someone you know already fallen victim to a scam? Don't worry. Fill out this basic info, and the AI will draft an official complaint text for you.")
    
    col1, col2 = st.columns(2)
    with col1:
        victim_name = st.text_input("Victim's Name:")
        fraud_type = st.selectbox("Type of Fraud Faced:", ["Financial Fraud (Online Banking/UPI)", "Fake Lottery/Job Scam", "Social Media Identity Theft/Hacking", "Other Cyber Crime"])
    with col2:
        amount_lost = st.text_input("Amount Lost (If applicable):", placeholder="e.g., Rs. 5000")
        date_of_incident = st.date_input("Date of Incident:")

    if st.button("Draft Complaint Guide", key="btn_complaint"):
        if victim_name:
            with st.spinner("Drafting your step-by-step complaint guide..."):
                prompt = f"""
                The user named {victim_name} faced a cyber fraud of type '{fraud_type}' losing around {amount_lost} on {date_of_incident}.
                Generate a clear step-by-step guide in simple English explaining how they can file an official complaint on the Indian Cybercrime portal (cybercrime.gov.in) or by calling 1930.
                Also, provide a ready-to-copy, well-structured incident description text in formal English that they can directly copy-paste into the government portal's description box.
                """
                ai_result = analyze_with_ai(prompt)
                st.info("📝 Your Personalized Cyber Complaint Guide:")
                st.write(ai_result)
        else:
            st.info("Please fill in at least the Victim's Name to draft the guide.")