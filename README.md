# PyBuddy – Personal Python Question-Answering Chatbot

## 1. Project Overview

PyBuddy is an AI-powered Python question-answering chatbot developed using Python, Streamlit, and Google's Gemini API. It helps users learn Python programming by answering questions in beginner-friendly language and providing code examples.

The chatbot includes a local Python knowledge base that provides predefined notes on common Python topics. When a question matches a topic, the relevant notes are included in the prompt sent to Gemini.

## 2. Objectives

- Build an interactive chatbot for Python-related questions.
- Provide understandable explanations and programming examples.
- Use a local knowledge base containing predefined Python notes.
- Maintain conversation history for future reference.
- Handle common API and connection errors gracefully.
- Provide a simple, user-friendly web interface.

## 3. Technologies Used

- **Python:** Application logic and knowledge-base search.
- **Streamlit:** Web interface and interactive chat.
- **Google Gemini API:** AI-powered answer generation.
- **JSON:** Local storage of chat history.
- **python-dotenv:** Securely load the API key from an environment file.

## 4. Main Features

- AI-powered Python question answering.
- Local Python knowledge base.
- Beginner-friendly explanations and code examples.
- Persistent chat history stored locally.
- New chat creation and conversation selection.
- Suggested Python questions.
- Error messages for common API failures.
- Responsive, ChatGPT-inspired interface.

## 5. Knowledge Base Topics

The local knowledge base contains notes on:

- Python introduction
- Variables and data types
- Conditional statements
- Loops and functions
- Lists, tuples, and dictionaries
- Object-oriented programming
- Exception handling
- File handling
- Modules
- List comprehension
- Lambda functions
- Recursion

## 6. Project Structure

```text
Python_Chatbot/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── chat_history.json
```

The `.env` file stores the Gemini API key and must not be shared publicly. The `chat_history.json` file is created when conversations are saved.

## 7. Installation and Setup

### Prerequisites

- Python 3.11 or a compatible Python version
- A Google Gemini API key
- Internet connection
- Visual Studio Code or another Python editor

### Step 1: Install dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Configure the API key

Create a `.env` file in the project directory and add:

```text
GEMINI_API_KEY=your_actual_api_key
```

Replace the placeholder with your own valid Gemini API key. Never upload the actual key to GitHub.

### Step 3: Run the application

Run:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 8. How It Works

1. The user enters a Python question in the chat interface.
2. PyBuddy searches its local Python knowledge base for a relevant topic.
3. If a matching topic is found, its notes are included in the prompt.
4. The prompt is sent to the Gemini API.
5. Gemini generates an answer.
6. The response is displayed in the chat interface.
7. The conversation is saved locally as JSON.

If no local topic matches, the chatbot can still use Gemini's general knowledge to answer the question.

## 9. Error Handling

The application includes checks for a missing API key, Gemini client initialization problems, empty responses, API quota issues, network failures, and unexpected errors.

Friendly messages help users understand common problems without exposing technical error details by default.

## 10. Limitations

- An internet connection is required for Gemini-generated answers.
- API usage is subject to the applicable Gemini API limits and policies.
- The local knowledge base covers a predefined set of Python topics.
- Chat history is stored locally and is not automatically synchronized across devices.
- AI-generated answers may occasionally be incomplete or incorrect.

## 11. Future Enhancements

- Expand the Python knowledge base with additional topics.
- Add document-based question answering.
- Support Python code debugging and error explanations.
- Add user feedback and answer ratings.
- Improve knowledge retrieval using semantic search.
- Add automated testing and usage analytics.

## 12. Conclusion

PyBuddy demonstrates how Python, a local knowledge base, and a generative AI API can be combined to build an interactive programming assistant. It provides a simple platform for learning Python concepts and exploring code examples through a conversational interface.
