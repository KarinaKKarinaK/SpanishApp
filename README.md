! Change the OPENAI_API_KEY value in the .env-example file for your own API key.

A Spanish language learning web application built using Python, Streamlit, and OpenAI API, designed to help students practice speaking, listening, reading, and writing through interactive tools.

🔧 Features
- Authentication: Secure login & registration with SHA256 password hashing and SQLite DB.
- Language Tools:
    - ChatBot – Text-based Spanish conversation simulation.
    - AudioBot – Speech-to-text + TTS interaction using gTTS.
    - Summarizer – Abstracts key content from Spanish input.
    - Translator – Translates between Spanish and other languages.
    - Concept Simplifier – Reduces complex Spanish input into simpler explanations.
    - Note Generator – Produces structured notes from user prompts.
    - Keyword Finder – Extracts main keywords from Spanish text.
- User Interface:
    - Sidebar-based navigation
    - Responsive layout
    - Spanish-only language environment
    - Minimalist design with white/black/green theme

🛠 Tech Stack
- Backend: Python, SQLite
- Frontend: Streamlit
- AI Integration: OpenAI GPT-3.5/DaVinci models (openai library)
- TTS: Google Text-to-Speech (gTTS)
- Security: hashlib for password hashing

--> Setup Instructions:
1. Clone repo: 
git clone https://github.com/your-username/espanol-interactivo.git
cd espanol-interactivo
2. Install dependencies:
pip install streamlit openai gtts python-dotenv
3. Run teh app:
streamlit run Inicio.py
