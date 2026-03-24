import random
import string
from collections import deque
 
# ──────────────────────────────────────────────
#  Store last 3 checked passwords (history)
# ──────────────────────────────────────────────
history = deque(maxlen=3)
 
 
# ══════════════════════════════════════════════
#  SECTION 1 – Password Generator
# ══════════════════════════════════════════════
 
def generate_password(length):
    """Generate a random password with letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
 
 
# ══════════════════════════════════════════════
#  SECTION 2 – Strength Checker (scoring logic)
# ══════════════════════════════════════════════
 
def check_strength(password):
    score = 0
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 2
    elif len(password) >= 6:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2
    common_patterns = ["123", "password", "abc", "qwerty", "111", "000"]
    for pattern in common_patterns:
        if pattern in password.lower():
            score -= 2
    return max(0, min(score, 10))
 
 
# ══════════════════════════════════════════════
#  SECTION 3 – Analyser
# ══════════════════════════════════════════════
 
def analyze_password(password):
    score = check_strength(password)
    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    else:
        strength = "Strong"
    suggestions = []
    if len(password) < 8:
        suggestions.append("Increase password length to at least 8 characters")
    if not any(c.isupper() for c in password):
        suggestions.append("Add at least one UPPERCASE letter")
    if not any(c.islower() for c in password):
        suggestions.append("Add at least one lowercase letter")
    if not any(c.isdigit() for c in password):
        suggestions.append("Add at least one digit (0-9)")
    if not any(c in string.punctuation for c in password):
        suggestions.append("Add at least one special character (!@#$...)")
    return strength, score, suggestions
 
 
# ══════════════════════════════════════════════
#  SECTION 4 – History
# ══════════════════════════════════════════════
 
def add_to_history(password, strength):
    history.append((password, strength))
 
def show_history():
    if not history:
        print("\n  No history yet - check a password first.")
        return
    print("\n--- Last Checked Passwords ---")
    for idx, (p, s) in enumerate(history, 1):
        masked = p[:2] + "*" * (len(p) - 4) + p[-2:] if len(p) > 4 else p
        print(f"  {idx}. {masked:<25} -> {s}")
 
 
# ══════════════════════════════════════════════
#  SECTION 5 – Helpers
# ══════════════════════════════════════════════
 
def print_header():
    print("""
===== PASSWORD SECURITY TOOLKIT =====
  1.  Generate a Password
  2.  Check Password Strength
  3.  Show History
  4.  Exit
======================================""")
 
def draw_score_bar(score, out_of=10):
    filled = int((score / out_of) * 20)
    bar = "#" * filled + "-" * (20 - filled)
    return f"[{bar}]  {score}/{out_of}"
 
 
# ══════════════════════════════════════════════
#  SECTION 6 – Main Menu
# ══════════════════════════════════════════════
 
def main():
    print("\n  Welcome to the Password Security Toolkit!")
    while True:
        print_header()
        choice = input("  Enter choice (1-4): ").strip()
 
        if choice == '1':
            try:
                length = int(input("\n  Enter desired password length (8-64): "))
                if not (8 <= length <= 64):
                    print("  Please enter a length between 8 and 64.")
                    continue
                password = generate_password(length)
                print(f"\n  Generated Password : {password}")
                print(f"  Length             : {length} characters")
            except ValueError:
                print("  Invalid input - please enter a number.")
 
        elif choice == '2':
            password = input("\n  Enter password to check: ")
            if not password:
                print("  Password cannot be empty.")
                continue
            strength, score, suggestions = analyze_password(password)
            print(f"\n  Password  : {password}")
            print(f"  Strength  : {strength}")
            print(f"  Score     : {draw_score_bar(score)}")
            if suggestions:
                print("\n  Suggestions to improve:")
                for tip in suggestions:
                    print(f"    - {tip}")
            else:
                print("\n  Your password looks great - no suggestions!")
            add_to_history(password, strength)
 
        elif choice == '3':
            show_history()
 
        elif choice == '4':
            print("\n  Exiting... Stay secure!\n")
            break
 
        else:
            print("  Invalid choice - please enter 1, 2, 3, or 4.")
 
        input("\n  Press Enter to continue...")
 
if __name__ == "__main__":
    main()