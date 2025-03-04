import re
import random
import string
import streamlit as st

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
st.title("🔐 Password Strength Checker")
password = st.text_input("Enter your password:", type="password")

if st.button("Check Strength"):
    if password:
        result = check_password_strength(password)
        st.write(result)
    else:
        st.warning("Please enter a password to check.")

if st.button("Generate Strong Password"):
    st.write("Suggested Strong Password:", generate_strong_password())
