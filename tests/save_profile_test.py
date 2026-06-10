from agents.profile_agent import profile_agent
from dotenv import load_dotenv
from memory.memory import save_profile, get_profile

load_dotenv()



profile = profile_agent("Hi AiDA, I am Adrien, 22 yo, 175cm, and 90kg. I like basketball. I have dumbells at home. I like strenght workout, dislike cardio. I like sweeted dishes. And I have a knee injury.")

print(profile)

profile_id = save_profile(profile)

print("\n\n")
retrieved_profile = get_profile(profile_id)
print(retrieved_profile)
