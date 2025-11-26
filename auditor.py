import google.generativeai as genai
import PIL.Image
import os

# --- PASTE YOUR KEY HERE ---
GOOGLE_API_KEY = "AIzaSyB80_hTQ3lu6yvz4uj-q5xAgKe25OQBb8k"

genai.configure(api_key=GOOGLE_API_KEY)

# --- THE FIX ---
# We are using a model explicitly found in your list:
model = genai.GenerativeModel('models/gemini-2.0-flash')

def analyze_site_safety(image_name):
    # Auto-add extension if missing
    if not image_name.endswith(('.jpg', '.png', '.jpeg')):
        image_name += ".jpg"

    print(f"🕵️  Looking for file: {image_name}")

    if not os.path.exists(image_name):
        print(f"❌ Error: File '{image_name}' not found.")
        print("Files in this folder:", [f for f in os.listdir() if f.endswith(('.jpg', '.png'))])
        return

    try:
        print("🚀 Sending to Gemini 2.0 (this is fast)...")
        img = PIL.Image.open(image_name)

        prompt = """
        You are a Senior Industrial Safety Officer. 
        Analyze this image strictly for safety hazards.
        
        Output a report in this format:
        1. **Hazard:** [Name of hazard]
        2. **Severity:** [High/Medium/Low]
        3. **Recommendation:** [Action to fix]
        
        If the image looks safe, say "No immediate hazards detected."
        """

        response = model.generate_content([prompt, img])
        
        print("\n" + "="*30)
        print("📝 SITE SAFETY AUDIT")
        print("="*30)
        print(response.text)
        
    except Exception as e:
        print(f"❌ AI Error: {e}")

# --- RUN IT ---
print("\n--- SiteSafe Auditor (Powered by Gemini 2.0) ---")
# List available files
files = [f for f in os.listdir() if f.endswith(('.jpg', '.png'))]
if files:
    print("Found images:", files)
else:
    print("⚠️ No images found! Please save a .jpg file in this folder.")

user_input = input("Enter image name: ")
analyze_site_safety(user_input)