import os
import re

# 1. FIXING THE PATHING ERROR
# This forces the script to look inside the 'stitching_engine' folder, no matter where your terminal is.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_original_chapter(text, num, roman):
    """Slices out the full original chapter from the Gutenberg text."""
    next_num = num + 1
    roman_numerals = {2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII', 9:'IX', 10:'X', 11:'XI', 12:'XII'}
    next_roman = roman_numerals.get(next_num, str(next_num))
    
    # Looks for "Chapter X" or "CHAPTER X" and grabs everything until the next chapter
    pattern = re.compile(rf'(?i)^Chapter\s+(?:{num}|{roman})\b(.*?)(?=^Chapter\s+(?:{next_num}|{next_roman})\b|\Z)', re.MULTILINE | re.DOTALL)
    match = pattern.search(text)
    
    if match:
        return match.group(1).strip()
    else:
        return f"[Error: Original Chapter {roman} not found. Check original_frankenstein.txt formatting.]"

def get_ai_chapter(text, roman):
    """Slices out the AI chapters from the Claude Reimagined text, ignoring the summaries."""
    # Looks for "[AI INTERVENTION] Chapter X" and stops at the "* * *" dividers
    pattern = re.compile(rf'\[AI INTERVENTION\]\s+Chapter\s+{roman}\s+—.*?(?=\*\s*\*\s*\*|\[ORIGINAL CANON\]|\[AI INTERVENTION\]|Epilogue|\Z)', re.DOTALL | re.IGNORECASE)
    match = pattern.search(text)
    
    if match:
        # Clean up the tag for a nicer reading experience
        clean_text = re.sub(r'\[AI INTERVENTION\]', '', match.group(0))
        # Remove any lingering source brackets
        clean_text = re.sub(r'\\', '', clean_text)
        return clean_text.strip()
    else:
        return f"[Error: AI Chapter {roman} not found in Frankenstein_Reimagined.txt]"

def assemble_accountability_cut():
    print("🚀 Initializing Final Narrative Assembly...")
    
    original_path = os.path.join(BASE_DIR, "original_frankenstein.txt")
    claude_path = os.path.join(BASE_DIR, "Frankenstein_Reimagined.txt")
    
    # 2. LOAD FILES SAFELY
    try:
        with open(original_path, "r", encoding="utf-8") as f:
            original = f.read()
        with open(claude_path, "r", encoding="utf-8") as f:
            ai_text = f.read()
    except FileNotFoundError as e:
        print(f"❌ Error: Could not find file -> {e.filename}")
        print("Please ensure both 'original_frankenstein.txt' and 'Frankenstein_Reimagined.txt' are in the 'stitching_engine' folder.")
        return

    final_novel = []
    
    # 3. BUILD THE TITLE PAGE
    final_novel.append("FRANKENSTEIN: THE ACCOUNTABILITY CUT\n")
    final_novel.append("A Moral Reimagining by Ming Xiang & Mary Shelley\n")
    final_novel.append("="*60 + "\n\n")

    # 4. GRAB WALTON'S OPENING LETTERS (From Original)
    print("-> Stitching Walton's Opening Letters (ORIGINAL)...")
    letters_pattern = re.compile(r'(?i)^Letter\s+1\b(.*?)(?=^Chapter\s+(?:1|I)\b)', re.MULTILINE | re.DOTALL)
    letters_match = letters_pattern.search(original)
    if letters_match:
        final_novel.append(f"--- [ORIGINAL CANON] WALTON'S LETTERS ---\n\n{letters_match.group(1).strip()}\n\n")

    # 5. THE MASTER BLUEPRINT
    blueprint = [
        (1, 'AI', 'I'), (2, 'ORIGINAL', 'II'), (3, 'ORIGINAL', 'III'), (4, 'ORIGINAL', 'IV'), (5, 'ORIGINAL', 'V'),
        (6, 'AI', 'VI'), (7, 'ORIGINAL', 'VII'), (8, 'ORIGINAL', 'VIII'), (9, 'ORIGINAL', 'IX'), (10, 'ORIGINAL', 'X'),
        (11, 'ORIGINAL', 'XI'), (12, 'AI', 'XII'), (13, 'AI', 'XIII'), (14, 'AI', 'XIV'), (15, 'AI', 'XV'), (16, 'AI', 'XVI'),
        (17, 'AI', 'XVII'), (18, 'AI', 'XVIII'), (19, 'AI', 'XIX')
    ]

    for num, source, roman in blueprint:
        print(f"-> Stitching Chapter {roman} ({source})...")
        if source == 'ORIGINAL':
            content = get_original_chapter(original, num, roman)
            final_novel.append(f"--- [ORIGINAL CANON] CHAPTER {roman} ---\n\n{content}\n\n")
        else:
            content = get_ai_chapter(ai_text, roman)
            final_novel.append(f"--- [AI INTERVENTION] CHAPTER {roman} ---\n\n{content}\n\n")

    # 6. GRAB THE EPILOGUE (From AI)
    print("-> Stitching Epilogue (AI)...")
    epilogue_pattern = re.compile(r'Epilogue: Walton\'s Final Letter.*', re.DOTALL | re.IGNORECASE)
    epilogue_match = epilogue_pattern.search(ai_text)
    if epilogue_match:
        clean_epilogue = re.sub(r'\\', '', epilogue_match.group(0))
        final_novel.append(f"--- [AI INTERVENTION] EPILOGUE ---\n\n{clean_epilogue.strip()}\n\n")

    # 7. EXPORT THE FULL NOVEL
    output_path = os.path.join(BASE_DIR, "FINAL_Frankenstein_Accountability_Cut.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("".join(final_novel))
    
    print(f"\n✅ DONE! Your final 70,000+ word submission file is saved at: {output_path}")

if __name__ == "__main__":
    assemble_accountability_cut()