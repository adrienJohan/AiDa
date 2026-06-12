
## 3. File Breakdown

### Front-End & UI Components

- **app.py**: The primary entry point for the Streamlit web interface. It handles top-level routing (Landing, Onboarding, Mission Control) and global state initialization.
- **ui.py**: A shared utility file containing reusable Streamlit UI components (cards, custom CSS injection, data frames rendering) and layout helpers (sidebar, spacers).
- **pages/Coach.py**: Interface for the general chat-based coaching flow. Handles displaying chat history, chat input, conversational layout, and quick-action chips.
- **pages/Nutrition.py**: Interface tailored for nutritional analysis. Includes UI for text-based meal logging and an integrated camera dialog for image-based meal inference.
- **pages/Progress.py**: Dashboard interface showcasing tracking charts, weight update functionality, and progression tracking visually.
- **pages/Workout.py**: Interface for displaying and tracking completion of AI-generated workout routines and planning.
- **pages/Profile.py**: Interface viewing user settings, personal metrics, and high-level profile goals.

### Core Systems & Data Access (Backend)

- **database/db.py**: Provides the foundational SQLite database initialization logic and table schemas (creating tables if missing).
- **memory/memory.py**: The primary data access object (DAO). It encompasses all `save_` and `get_` database interactions handling User Profiles, Workout Sessions, Current Meals, Weight Logs, and Conversation History.
- **core/session.py**: Utilities managing the temporal conversational state machine. Retrieves and mutates the current active mode or intent within the system runtime.

### AI Execution Logic (Agents)

- **agents/orchestrator.py**: The central brain of the conversational flow. Receives user inputs, determines the intent (using `route_intent`), and delegates the task to the appropriate specialized workflow.
- **agents/response_agent.py**: Applies dynamic "humanizing" variations, dynamically standardizing the tone and natural feel of system text boundaries using the Google GenAI interface.
- **agents/nutrition_agent.py | image_meal_agent.py**: Specific agents prompting the LLM for structured meal planning and vision-based calorie/macronutrient extractions from photos.
- **agents/workout_agent.py**: Connects to the LLM to generate structured JSON routines given user constraints.
- **agents/analyst_agent.py | weekly_report_agent.py**: Evaluates historical data aggregations to formulate user feedback and comprehensive weekly progression check-ins.
- **agents/profile_agent.py | field_extractor.py**: Specialized for iterating over missing profile fields to complete the initial user onboarding context.

### Workflows (Business Logic)

Workflows organize the transitions between the user and the disparate back-end agents:

- **workflows/onboarding.py**: State machine iterating over required fields until the user profile configuration is completed.
- **workflows/chat.py & workflows/coach.py**: Intermediaries mapping unstructured conversational strings to the AI coach endpoints and storing messages iteratively to memory.
- **workflows/nutrition.py | nutrition_router.py**: Distinguishes intent within the nutritional domain (planning vs logging) and dispatches either vision analysis or contextual text extraction paths.
- **workflows/weight_update.py & workflows/weekly_report.py**: Handle logging numerical inputs cleanly and executing chron-style review tasks respectively.

## 4. Data & State Flow

1. **User Interacts (UI Layer)**: The user visits Streamlit (`app.py` or `pages/*`) and triggers a component click or sends a chat message.

2. **Session & Intent Inspection**: Context dictates behavior depending on `core/session.py`. If active mode dictates standard chat, the prompt is forwarded to `agents/orchestrator.py`.

3. **Routing**: The Orchestrator determines intent natively or calls the Gemini API classifying the immediate need. Control is handed to the appropriate state controller within `workflows/`.

4. **Generation & Manipulation**: The chosen Workflow utilizes single-function `agents/` scripts to execute GenAI text and multimodal capabilities precisely (e.g., converting a meal image to a JSON array of specific macronutrients).

5. **State Persistence & Response**: Information payload updates local session pointers. Concrete details (e.g., tracking a meal, saving a chat, completing a workout target) are pushed asynchronously via `memory/memory.py` to the SQLite engine (`aida.db`).

6. **UI Refresh**: With the database and chat history updated, the `ui.py` elements instantly map the re-render state loop to display formatted notifications, modified charts, or humanized textual dialogue inside the chat feed to the user.