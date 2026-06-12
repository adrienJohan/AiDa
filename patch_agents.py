import os
import glob
import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Skip if already patched
    if "from agents.llm_client import generate_with_fallback" in content:
        return False

    orig_content = content
    
    # 1. Add import right after import genai
    content = re.sub(
        r'(from google import genai)', 
        r'\1\nfrom agents.llm_client import generate_with_fallback', 
        content
    )
    
    # Alternatively if it relies on "import google.generativeai" or similar
    if "from agents.llm_client import generate_with_fallback" not in content and "import" in content:
        # just prepend it
        content = "from agents.llm_client import generate_with_fallback\n" + content

    # 2. Patch client.models.generate_content
    # It looks like: client.models.generate_content(
    # Because of indentation we should match appropriately
    # We replace "client.models.generate_content(" with "generate_with_fallback("
    content = content.replace("client.models.generate_content(", "generate_with_fallback(")
    
    if content != orig_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

if __name__ == "__main__":
    agents_dir = os.path.join(os.path.dirname(__file__), "agents")
    files = glob.glob(os.path.join(agents_dir, "*.py"))
    
    count = 0
    for f in files:
        if os.path.basename(f) not in ["llm_client.py", "__init__.py"]:
            if patch_file(f):
                count += 1
                print(f"Patched {f}")
    
    print(f"Patched {count} files.")
