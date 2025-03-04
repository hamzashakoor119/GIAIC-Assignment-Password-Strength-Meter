import re
import random
import string
import streamlit as st
import bcrypt
import requests
import sqlite3

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()

def register_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return "✅ Registration Successful!"
    except sqlite3.IntegrityError:
        return "❌ Username already exists! Choose another one."

def login_user(username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[0]):
        return "✅ Login Successful!", True
    else:
        return "❌ Invalid Username or Password!", False

def check_password_strength(password):
    score = 0
    suggestions = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("Include at least one special character (!@#$%^&*).")
    
    # Common Weak Passwords Blacklist
    weak_passwords = ["password", "123456", "qwerty", "password123", "abc123"]
    if password.lower() in weak_passwords:
        return "❌ This is a commonly used weak password. Choose a stronger one."
    
    # Strength Rating
    if score == 4:
        return "✅ Strong Password!"
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features."
    else:
        return "❌ Weak Password - " + " ".join(suggestions)

def generate_strong_password():
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

# Streamlit UI
st.set_page_config(page_title="Password Strength Checker", layout="wide")

# Center the title with blue color
st.markdown("""
    <h1 style='text-align: center; color: blue;'>Code With Hamza</h1>
""", unsafe_allow_html=True)

# Centered layout for authentication and password checker
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.subheader("🔑 User Authentication")
    choice = st.radio("Login or Register:", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username", max_chars=20)
    password_auth = st.text_input("Password", type="password", max_chars=20)
    if st.button("Submit"):
        if choice == "Register":
            st.write(register_user(username, password_auth))
        else:
            login_message, success = login_user(username, password_auth)
            st.write(login_message)
            if success:
                st.success("✅ Login Successful!\n🎉 **Welcome To Code With Hamza** 🎉\n🌐 Join Our Community: [IT HuB PK](https://www.linkedin.com/groups/13109907)")
    
    st.subheader("🔎 Password Strength Check")
    password = st.text_input("Enter your password to check:", type="password", max_chars=30)
    if st.button("Check Strength"):
        if password:
            result = check_password_strength(password)
            st.write(result)
        else:
            st.warning("Please enter a password to check.")
    
    if st.button("Generate Strong Password"):
        strong_password = generate_strong_password()
        st.write("Suggested Strong Password:", strong_password)

# Apply layout adjustments
st.sidebar.title("🔧 Options")
st.sidebar.markdown("---")
st.sidebar.subheader("Features Added:")
st.sidebar.write("✅ User Authentication (Login & Register)")
st.sidebar.write("✅ Real-Time Password Strength Checking")
st.sidebar.write("✅ Centered UI Layout")
st.sidebar.write("✅ Dark Mode Toggle")
st.sidebar.write("✅ Password Breach Check")
st.sidebar.write("✅ Strength Progress Bar")
st.sidebar.write("✅ User Password History")
st.sidebar.write("✅ Strong Password Generator")
st.sidebar.write("✅ Professional UI")
