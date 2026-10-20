
import os
import json
import uuid
from pathlib import Path
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ==========================================
# 1. CONFIGURATION
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-flash-lite-latest"

HISTORY_FILE = Path(__file__).parent / "chat_history.json"

st.set_page_config(
    page_title="PyBuddy - Python AI Assistant",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. PYTHON KNOWLEDGE BASE
# ==========================================

PYTHON_KNOWLEDGE_BASE = {
    "python introduction": """
Python is a high-level, interpreted programming language.
It has readable syntax and is used in automation, web development,
data science, artificial intelligence, and machine learning.
""",

    "variables": """
Variables store data values.

Example:
name = "Ashwini"
age = 21
marks = 85.5

Python automatically determines the variable's data type.
""",

    "data types": """
Common Python data types:
- int: Whole numbers, such as 10
- float: Decimal numbers, such as 10.5
- str: Text, such as "Hello"
- bool: True or False
- list: Ordered, changeable collection
- tuple: Ordered, unchangeable collection
- dict: Key-value pairs
- set: Collection of unique items
""",

    "conditional statements": """
Conditional statements execute code based on conditions.
Python uses if, elif, and else.

Example:
age = 18

if age >= 18:
    print("Adult")
else:
    print("Minor")
""",

    "loops": """
Loops repeat a block of code.

For loop:
for i in range(5):
    print(i)

While loop:
i = 0
while i < 5:
    print(i)
    i += 1
""",

    "functions": """
Functions are reusable blocks of code.
Python defines functions using the def keyword.

Example:
def add(a, b):
    return a + b

print(add(5, 3))
Output: 8
""",

    "lists": """
Lists store multiple items in an ordered, changeable collection.

Example:
fruits = ["apple", "banana", "mango"]
print(fruits[0])
fruits.append("orange")
""",

    "tuples": """
Tuples store multiple items in an ordered collection.
They cannot be changed after creation.

Example:
coordinates = (10, 20)
print(coordinates[0])
""",

    "dictionaries": """
Dictionaries store data as key-value pairs.

Example:
student = {
    "name": "Ashwini",
    "age": 21,
    "branch": "AI and Data Science"
}

print(student["name"])
""",

    "object oriented programming": """
Object-oriented programming organizes code using classes and objects.
Important concepts include classes, objects, inheritance,
encapsulation, and polymorphism.

Example:
class Student:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)

student = Student("Ashwini")
student.display()
""",

    "exception handling": """
Exception handling manages runtime errors.
Python uses try and except.

Example:
try:
    number = int(input("Enter a number: "))
    print(10 / number)
except ZeroDivisionError:
    print("Cannot divide by zero.")
except ValueError:
    print("Enter a valid integer.")
""",

    "file handling": """
File handling allows Python to read and write files.

Example:
with open("example.txt", "w") as file:
    file.write("Hello Python!")

with open("example.txt", "r") as file:
    print(file.read())
""",

    "modules": """
Modules are Python files containing reusable code.

Example:
import math
print(math.sqrt(25))

Output: 5.0
""",

    "list comprehension": """
List comprehension creates lists concisely.

Example:
squares = [x * x for x in range(1, 6)]
print(squares)

Output: [1, 4, 9, 16, 25]
""",

    "lambda functions": """
Lambda functions are small anonymous functions.

Example:
add = lambda a, b: a + b
print(add(2, 3))

Output: 5
""",

    "recursion": """
Recursion occurs when a function calls itself.

Example:
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))

Output: 120
"""
}


def search_python_knowledge(question):
    """Search for a matching topic in the local knowledge base."""

    question_lower = question.lower()

    for topic, information in PYTHON_KNOWLEDGE_BASE.items():
        if topic in question_lower:
            return information

    keywords = {
        "variable": "variables",
        "datatype": "data types",
        "data type": "data types",
        "condition": "conditional statements",
        "if statement": "conditional statements",
        "for loop": "loops",
        "while loop": "loops",
        "function": "functions",
        "list": "lists",
        "tuple": "tuples",
        "dictionary": "dictionaries",
        "dict": "dictionaries",
        "oop": "object oriented programming",
        "class": "object oriented programming",
        "object": "object oriented programming",
        "error": "exception handling",
        "exception": "exception handling",
        "file": "file handling",
        "module": "modules",
        "comprehension": "list comprehension",
        "lambda": "lambda functions",
        "recursion": "recursion",
        "factorial": "recursion",
    }

    for keyword, topic in keywords.items():
        if keyword in question_lower:
            return PYTHON_KNOWLEDGE_BASE[topic]

    return None


# ==========================================
# 3. CHAT HISTORY FUNCTIONS
# ==========================================

def load_chats():
    """Load previous chats safely."""

    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                return data

        except (json.JSONDecodeError, OSError):
            pass

    return {}


def save_chats():
    """Save chats without crashing the application."""

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.chats,
                file,
                indent=2,
                ensure_ascii=False
            )
        return True

    except OSError:
        return False


def create_chat():
    """Create a new chat."""

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": "New chat",
        "messages": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    st.session_state.current_chat_id = chat_id
    save_chats()


def get_current_chat():
    return st.session_state.chats[
        st.session_state.current_chat_id
    ]


# ==========================================
# 4. SESSION STATE
# ==========================================

if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

if st.session_state.current_chat_id not in st.session_state.chats:
    if st.session_state.chats:
        st.session_state.current_chat_id = next(
            iter(st.session_state.chats)
        )
    else:
        create_chat()


# ==========================================
# 5. INITIALIZE GEMINI CLIENT
# ==========================================

client = None

if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception:
        client = None


# ==========================================
# 6. ERROR HANDLING FUNCTIONS
# ==========================================

def get_friendly_error(error):
    """Convert common API errors into understandable messages."""

    error_text = str(error).lower()

    if any(word in error_text for word in [
        "api_key_invalid",
        "invalid api key",
        "api key not valid",
        "unauthorized",
        "permission denied",
        "401",
        "403"
    ]):
        return (
            "Your Gemini API key may be invalid or unauthorized. "
            "Check the GEMINI_API_KEY value in your .env file "
            "and verify that your key is active."
        )

    if any(word in error_text for word in [
        "resource_exhausted",
        "quota",
        "rate limit",
        "429",
        "too many requests"
    ]):
        return (
            "The Gemini API request limit or quota may have been "
            "reached. Check your API usage and limits, then try "
            "again later."
        )

    if any(word in error_text for word in [
        "deadline_exceeded",
        "timed out",
        "timeout",
        "connection",
        "network",
        "503",
        "unavailable",
        "500",
        "502"
    ]):
        return (
            "Gemini could not be reached right now. Check your "
            "internet connection and try again in a little while."
        )

    return (
        "An unexpected error occurred while generating your answer. "
        "Please try again. If the problem continues, check the "
        "technical details below."
    )


def generate_answer(question):
    """Generate an answer using local notes and Gemini."""

    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    if client is None:
        raise ValueError(
            "The Gemini client could not be initialized. "
            "Check your API key and package installation."
        )

    knowledge = search_python_knowledge(question)

    if knowledge:
        prompt = f"""
You are PyBuddy, a friendly Python programming tutor.

Use these local Python notes when they are relevant.

LOCAL PYTHON KNOWLEDGE:
{knowledge}

USER QUESTION:
{question}

Explain the answer in beginner-friendly language.
Provide a correct code example when useful.
If the notes do not contain enough information, use
your general Python knowledge.
"""
    else:
        prompt = f"""
You are PyBuddy, a friendly Python programming tutor.

Answer accurately and clearly in beginner-friendly language.
Include a code example when useful.

USER QUESTION:
{question}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    answer = response.text

    if not answer or not answer.strip():
        raise RuntimeError(
            "Gemini returned an empty response. Please try again."
        )

    return answer.strip()


# ==========================================
# 7. PAGE DESIGN
# ==========================================

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    .stApp {
        background-color: #212121;
        color: #ECECEC;
    }

    [data-testid="stSidebar"] {
        background-color: #171717;
    }

    [data-testid="stSidebar"] * {
        color: #ECECEC;
    }

    .main-title {
        font-size: 34px;
        font-weight: 700;
        text-align: center;
        margin-top: 80px;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #B4B4B4;
        margin-bottom: 30px;
    }

    [data-testid="stChatInput"] {
        background-color: #303030;
        border-radius: 20px;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 17px !important;
    }

    .stButton button {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# 8. SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("## 🐍 PyBuddy")
    st.caption("Your Python AI Assistant")

    if st.button("＋ New chat", use_container_width=True):
        create_chat()
        st.rerun()

    st.divider()
    st.markdown("### Chat history")

    chat_ids = sorted(
        st.session_state.chats.keys(),
        key=lambda chat_id: st.session_state.chats[
            chat_id
        ].get("created_at", ""),
        reverse=True
    )

    for chat_id in chat_ids:
        chat = st.session_state.chats[chat_id]
        title = chat.get("title", "New chat")

        if st.button(
            f"💬 {title[:35]}",
            key=f"chat_{chat_id}",
            use_container_width=True
        ):
            st.session_state.current_chat_id = chat_id
            st.rerun()

    st.divider()
    st.markdown("### Python topics")

    st.markdown(
        """
        - Python basics
        - Variables and data types
        - Conditional statements
        - Loops and functions
        - Lists, tuples and dictionaries
        - Object-oriented programming
        - Exception handling
        - File handling
        - Recursion and lambda
        """
    )

    st.divider()

    if st.button("🗑️ Clear all chat history", use_container_width=True):
        st.session_state.chats = {}
        create_chat()
        st.rerun()


# ==========================================
# 9. MAIN CHAT WINDOW
# ==========================================

current_chat = get_current_chat()

if not current_chat["messages"]:

    st.markdown(
        '<div class="main-title">What can I help you learn?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Ask anything about Python programming.'
        '</div>',
        unsafe_allow_html=True
    )

    columns = st.columns(2)

    suggestions = [
        "Explain Python variables with examples",
        "What is the difference between a list and tuple?",
        "Explain loops in Python",
        "Teach me object-oriented programming"
    ]

    for index, suggestion in enumerate(suggestions):
        with columns[index % 2]:
            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True
            ):
                st.session_state.pending_question = suggestion
                st.rerun()

else:
    st.markdown("## PyBuddy")

    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# ==========================================
# 10. USER INPUT AND RESPONSE
# ==========================================

user_question = st.chat_input("Message PyBuddy...")

if "pending_question" in st.session_state:
    user_question = st.session_state.pop("pending_question")

if user_question:

    user_question = user_question.strip()

    if not user_question:
        st.warning("Please enter a question.")
        st.stop()

    current_chat = get_current_chat()

    current_chat["messages"].append({
        "role": "user",
        "content": user_question
    })

    if current_chat["title"] == "New chat":
        current_chat["title"] = user_question[:35]

    save_chats()

    with st.chat_message("user"):
        st.markdown(user_question)

    with st.chat_message("assistant"):

        try:
            with st.spinner("PyBuddy is thinking..."):
                answer = generate_answer(user_question)

            st.markdown(answer)

        except Exception as error:
            answer = get_friendly_error(error)

            st.error(answer)

            with st.expander("Technical details"):
                st.code(str(error))

            # Show an easy retry button.
            if st.button(
                "Try again",
                key=f"retry_{uuid.uuid4().hex}"
            ):
                st.session_state.pending_question = user_question
                st.rerun()

        current_chat["messages"].append({
            "role": "assistant",
            "content": answer
        })

        if not save_chats():
            st.warning(
                "Your response is visible, but chat history "
                "could not be saved to the local file."
            )

    st.rerun()
