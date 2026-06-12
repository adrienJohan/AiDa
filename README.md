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
You can install the required packages utilizing either standard PIP options using `pyproject.toml` or the included `requirements.txt` file. For a local editable installation, ensure your virtual environment is activated and run:

```bash
pip install -e .
```
Alternatively, using the requirements file explicitly:
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Ensure you have a `.env` file in the base directory of the project containing the required API credentials. It should look like this:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the Application
Finally, start the Streamlit application by running the following command:

```bash
stramlit run app.py
```

## Architecture and Design
For more insights into the internal architecture, state flow, and system components layout, please consult the [`ARCHITECTURE.md`](ARCHITECTURE.md) document.
