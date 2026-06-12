from agents.weight_agent import extract_weight_update
from dotenv import load_dotenv

load_dotenv()
msg = "Hi Aida, how are you today? For me, I am really excited about this new journey"
result = extract_weight_update(msg)
print("weight_update result:", result)
