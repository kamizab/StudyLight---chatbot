# StudyLight – LLM Quiz Chatbot

## 📑 Table of Contents

1. [Short Description (EN)](#short-description-en)  
2. [Extended Description (EN)](#extended-description-en)  
3. [Installation Guide (EN)](#installation-guide-en)  
4. [Krótki opis (PL)](#krótki-opis-pl)  
5. [Opis rozszerzony (PL)](#opis-rozszerzony-pl)  
6. [Instrukcja instalacji (PL)](#instrukcja-instalacji-pl)  
7. [Project Structure](#project-structure)  
8. [Security Notes](#security-notes)

---

## Short Description (EN)

StudyLight is a Streamlit-based chatbot application that generates interactive multiple-choice quizzes using an LLM (OpenAI or Gemini). The user provides a topic, additional details, and difficulty level, and the system generates a structured quiz with automatic grading and explanations.

---

## Extended Description (EN)

StudyLight is an educational web application built with Streamlit that integrates Large Language Models (LLMs) to dynamically generate quizzes in a conversational interface.

### Application workflow

1. The user selects a topic.
2. The chatbot asks for additional clarification.
3. The user sets a difficulty level (1–10).
4. The LLM generates a structured multiple-choice quiz (JSON format).
5. The user answers interactively.
6. The system calculates the score and displays explanations.

### Key features

- Structured JSON validation (Pydantic)
- Secure API key management via Streamlit Secrets
- Modular architecture (UI, state, LLM logic separation)
- Support for both OpenAI and Google Gemini

---

## Installation Guide (EN)

### 1️⃣ Clone the repository

```bash
git clone https://github.com/kamizab/StudyLight---chatbot.git
cd StudyLight---chatbot
```

### 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API keys

Create the folder:

```bash
mkdir .streamlit
```

Create the file:

```bash
touch .streamlit/secrets.toml
```

Example configuration (OpenAI):

```toml
PROVIDER = "openai"
OPENAI_API_KEY = "YOUR_API_KEY"
OPENAI_MODEL = "gpt-4.1-mini"
```

Example configuration (Gemini):

```toml
PROVIDER = "gemini"
GEMINI_API_KEY = "YOUR_API_KEY"
GEMINI_MODEL = "gemini-3-flash-preview"
```

⚠ Do **NOT** commit this file. It is excluded via `.gitignore`.

### 5️⃣ Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Krótki opis (PL)

StudyLight to aplikacja webowa oparta na Streamlit, która generuje interaktywne quizy wielokrotnego wyboru przy użyciu modelu językowego (OpenAI lub Gemini). Użytkownik podaje temat, doprecyzowanie oraz poziom trudności, a system generuje quiz z automatycznym sprawdzaniem odpowiedzi.

---

## Opis rozszerzony (PL)

StudyLight to aplikacja edukacyjna wykorzystująca modele LLM do dynamicznego generowania quizów w interfejsie konwersacyjnym.

### Przebieg działania

1. Użytkownik podaje temat quizu.
2. Chatbot prosi o doprecyzowanie.
3. Użytkownik wybiera poziom trudności (1–10).
4. Model językowy generuje quiz w ustrukturyzowanym formacie JSON.
5. Użytkownik odpowiada na pytania.
6. Aplikacja oblicza wynik i wyświetla wyjaśnienia.

### Główne cechy

- Walidacja odpowiedzi LLM (Pydantic)
- Bezpieczne przechowywanie kluczy API (Streamlit Secrets)
- Modularna architektura aplikacji
- Obsługa OpenAI i Gemini

---

## Instrukcja instalacji (PL)

### 1️⃣ Sklonuj repozytorium

```bash
git clone https://github.com/kamizab/StudyLight---chatbot.git
cd StudyLight---chatbot
```

### 2️⃣ Utwórz środowisko wirtualne (zalecane)

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3️⃣ Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4️⃣ Skonfiguruj klucz API

Utwórz folder `.streamlit` oraz plik `secrets.toml` zgodnie z konfiguracją podaną powyżej.

⚠ Plik ten nie powinien być dodawany do repozytorium.

### 5️⃣ Uruchom aplikację

```bash
streamlit run app.py
```

---

## Project Structure

```
StudyLight---chatbot/
│
├── app.py
├── pages/
│   └── 1_Quiz_Bot.py
│
├── src/
│   ├── state.py
│   ├── chat_flow.py
│   ├── quiz_engine.py
│   ├── llm_client.py
│   └── prompt_templates.py
│
├── .streamlit/
│   └── secrets.toml
│
├── requirements.txt
└── README.md
```

---

## Security Notes

- API keys are stored in `.streamlit/secrets.toml`
- The secrets file is excluded via `.gitignore`
- The application never logs or exposes API keys
- Structured validation ensures only correct JSON is accepted from the LLM