# AiDa - AI Fitness and Nutrition Coach

AiDa is an AI-powered tracking application designed to act as your personal fitness, nutrition, and well-being coach. Through a conversational web interface built on Streamlit, AiDa handles complex interactions from workout planning to logging meals using photo analysis. 

## Project Setup

To get the project up and running locally, please follow these steps:

### 1. Create a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies. Run the following in the project root:

```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# On Windows use: .venv\Scripts\activate
```

### 2. Install Dependencies
First, install the external dependencies required by the project:

```bash
pip install -r requirements.txt
```

### 3. Build & Install Local Modules
This step is **mandatory** for the application to function. Running this command installs the internal modules (`agents`, `memory`, `utils`, `core`, `workflows`) in editable mode, ensuring they are recognized as packages across the codebase and app:

```bash
pip install -e .
```

### 4. Setup Environment Variables
Ensure you have a `.env` file in the base directory of the project containing the required API credentials. It should look like this (at minimum):

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Obtaining a Gemini API Key:**
For security and privacy reasons, my personal API key cannot be distributed with this submission. You will need to provision your own key to run the application:
1. Navigate to [Google AI Studio](https://aistudio.google.com/).
2. Sign in using your Google account.
3. Click on the **"Get API key"** button on the left sidebar.
4. Generate a new API Key and copy it into your local `.env` file.

### 5. Run the Application
Finally, start the Streamlit application by running the following command:

```bash
streamlit run app.py
```

## API Integrations
For grading and evaluation purposes, the Gemini Generative AI API integrations can be found within the following directories:
- **`agents/`:** Contains the primary files handling requests to the LLM (e.g., `llm_client.py`, `orchestrator.py`, `image_meal_agent.py`).
- **`workflows/`:** Contains business logic flows utilizing the LLM (e.g., `chat.py`, `coach.py`).

## Architecture and Design
For more insights into the internal architecture, state flow, and system components layout, please consult the [`ARCHITECTURE.md`](ARCHITECTURE.md) document.
