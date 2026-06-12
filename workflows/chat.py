from google import genai
from dotenv import load_dotenv
from memory.memory import get_profile, get_recent_conversations
from core.session import get_profile_id, set_mode

load_dotenv()


def handle_chat_mode(user_message, session):
    """
    Handle free-form conversation with the user.
    Uses profile context and conversation history from the DB
    so AiDa can talk naturally and remember past exchanges.
    """

    profile_id = get_profile_id(session)
    profile = get_profile(profile_id) if profile_id else {}

    # ── Build profile context ───────────────────────────────────────
    profile_lines = []
    if profile:
        if profile.get("name"):
            profile_lines.append(f"Name: {profile['name']}")
        if profile.get("age"):
            profile_lines.append(f"Age: {profile['age']}")
        if profile.get("goal"):
            profile_lines.append(f"Goal: {profile['goal']}")
        if profile.get("weight"):
            profile_lines.append(f"Weight: {profile['weight']} kg")
        if profile.get("height"):
            profile_lines.append(f"Height: {profile['height']} cm")
        if profile.get("workout_equipment"):
            profile_lines.append(f"Equipment: {profile['workout_equipment']}")
        if profile.get("workout_preferences"):
            profile_lines.append(f"Workout prefs: {profile['workout_preferences']}")
        if profile.get("nutrition_preferences"):
            profile_lines.append(f"Nutrition prefs: {profile['nutrition_preferences']}")
        if profile.get("health_notes"):
            profile_lines.append(f"Health notes: {profile['health_notes']}")

    profile_block = "\n".join(profile_lines) if profile_lines else "No profile available."

    # ── Build conversation history from DB ──────────────────────────
    history_lines = []
    if profile_id:
        rows = get_recent_conversations(profile_id, limit=10)
        for user_msg, ai_msg in rows:
            history_lines.append(f"User: {user_msg}")
            history_lines.append(f"AiDa: {ai_msg}")

    history_block = "\n".join(history_lines) if history_lines else "No previous conversations."

    # ── Prompt ──────────────────────────────────────────────────────
    prompt = f"""You are AiDa, a personal fitness and nutrition AI coach.

Your personality:
- Supportive but realistic
- Action-oriented
- Warm and human, like a real coach talking to their client
- Never use emojis
- Never use excessive hype or generic motivational quotes

You are having a natural conversation with your client. You can talk about anything they want — fitness, life, motivation, questions, or just casual chat. You are not limited to fitness topics only. Be a genuinely helpful and engaging conversationalist.

However, you should always stay in character as their coach. If the conversation touches on fitness, nutrition, or their goals, draw on what you know about them.

If the user asks you to do something specific like creating a workout plan, logging a meal, or generating a report, let them know they can use the quick action buttons or ask directly for those tasks.

User profile:
{profile_block}

Recent conversation history:
{history_block}

Current message from user:
{user_message}

Respond naturally. Keep it concise (2-4 sentences unless the topic warrants more). Respond with ONLY the message text, nothing else."""

    client = genai.Client()

    response = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents=prompt,
    )

    # Reset to assistant mode so the next message gets re-routed
    set_mode(session, "assistant")

    return response.text.strip()
