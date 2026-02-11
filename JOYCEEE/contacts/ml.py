import re

def auto_category(name, notes=""):
    name_lower = name.lower()
    notes_lower = notes.lower()
    
    # Combine both name and notes for analysis
    combined_text = f"{name_lower} {notes_lower}"
    
    # Love/Relationship keywords (check in both name and notes)
    love_keywords = [
        "love", "babe", "baby", "honey", "sweetheart", "darling",
        "sweetie", "dearest", "my love", "hubby", "wifey",
        "girlfriend", "boyfriend", "partner", "significant other",
        "soulmate", "crush", "date"
    ]
    emojis = ["❤️", "💕", "😘"]
    
    # Family keywords
    family_keywords = [
        "mom", "dad", "father", "mother", "sister", "brother",
        "grandma", "grandpa", "aunt", "uncle", "cousin", "spouse",
        "wife", "husband", "son", "daughter", "parent", "family",
        "relative", "kin", "nephew", "niece"
    ]
    
    # Education keywords (moved up)
    education_keywords = [
        "teacher", "professor", "prof", "school", "university",
        "college", "student", "dean", "principal", "faculty",
        "tutor", "lecturer", "instructor", "educator", "academic",
        "classmate", "homework", "exam", "lesson", "campus"
    ]

    # Work keywords
    work_keywords = [
        "boss", "manager", "office", "work", "colleague",
        "ceo", "director", "supervisor", "company", "hr",
        "employee", "staff", "team", "corporate", "business",
        "client", "customer", "meeting", "project", "deadline"
    ]
    
    # Health keywords
    health_keywords = [
        "doctor", "dr", "nurse", "hospital", "clinic",
        "dentist", "physician", "therapist", "pharmacy",
        "patient", "appointment", "medical", "health", "emergency"
    ]

    def matches(keywords, emoji_list=None):
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', combined_text):
                return True
        if emoji_list:
            for em in emoji_list:
                if em in combined_text:
                    return True
        return False
    
    # Check for love/relationship terms FIRST (highest priority)
    if matches(love_keywords, emojis):
        return "Personal"
    
    # Then check other categories
    elif matches(family_keywords):
        return "Family"
    elif matches(education_keywords):
        return "Education"
    elif matches(work_keywords):
        return "Work"
    elif matches(health_keywords):
        return "Health"
    else:
        return "Personal"

# Test function (optional)
def test_categorization():
    test_cases = [
        ("Joyce", "Babe love of my life ❤️", "Personal"),
        ("John", "Babe my honey", "Personal"),
        ("Mom", "Call every Sunday", "Family"),
        ("Dr. Smith", "Annual checkup", "Health"),
        ("Office Manager", "Work project deadline", "Work"),
        ("Professor Lee", "Math class", "Education"),
        ("Sarah", "", "Personal"),  # No notes = default personal
    ]
    
    for name, notes, expected in test_cases:
        result = auto_category(name, notes)
        print(f"Name: {name}, Notes: {notes}")
        print(f"Expected: {expected}, Got: {result}, Match: {result == expected}\n")