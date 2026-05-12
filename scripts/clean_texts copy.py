#!/usr/bin/env python3
import re
import os
from pathlib import Path

def is_structural_noise(line):
    """
    Identifies lines that are likely Table of Contents, 
    isolated chapter/letter markers, or page headers.
    """
    # Common markers that don't contribute to 'prose style'
    noise_markers = ['CONTENTS', 'CHAPTER', 'LETTER', 'VOLUME', 'LIST OF', 'PREFACE']
    
    line_upper = line.strip().upper()
    
    # If the line is short and contains a noise marker, it's likely a header
    if len(line_upper) < 40 and any(marker in line_upper for marker in noise_markers):
        return True
    
    # Catch isolated Roman Numerals or digits (e.g., 'X.' or '12')
    if re.match(r'^[IVXLC\d]+[\.\s]*$', line_upper):
        return True
            
    return False

def clean_gutenberg_text(text):
    """
    Remove Project Gutenberg headers, footers, and structural noise.
    """
    text = text.replace('\ufeff', '')
    
    # 1. Strip Gutenberg Metadata
    start_markers = [r'\*\*\* START OF .+? \*\*\*', r'START OF THE PROJECT GUTENBERG EBOOK']
    end_markers = [r'\*\*\* END OF .+? \*\*\*', r'END OF THE PROJECT GUTENBERG EBOOK']
    
    start_pos = 0
    for marker in start_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            start_pos = match.end()
            break
            
    end_pos = len(text)
    for marker in end_markers:
        match = re.search(marker, text, re.IGNORECASE)
        if match:
            end_pos = match.start()
            break
    
    text = text[start_pos:end_pos]

    # 2. Filter lines for 'Structural Noise'
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Only keep the line if it ISN'T noise
        if not is_structural_noise(line):
            cleaned_lines.append(line)
    
    text = '\n'.join(cleaned_lines)
    
    # 3. Final Cleanup
    text = re.sub(r'Produced by .+?\n', '', text)
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)  # Keep 2 newlines for paragraph breaks
    text = re.sub(r'[ \t]+', ' ', text)
    
    return text.strip()

def process_files(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all .txt files in your current folder
    txt_files = list(input_path.glob('*.txt'))
    
    combined_file_path = output_path / "mary_shelley_combined.txt"
    
    with open(combined_file_path, 'w', encoding='utf-8') as master_file:
        for txt_file in txt_files:
            print(f"Cleaning: {txt_file.name}")
            with open(txt_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            clean_content = clean_gutenberg_text(content)
            
            # Save individual cleaned file
            with open(output_path / f"cleaned_{txt_file.name}", 'w', encoding='utf-8') as f:
                f.write(clean_content)
                
            # Add to the master file for training
            master_file.write(f"\n\n--- SOURCE: {txt_file.name} ---\n\n")
            master_file.write(clean_content)

    print(f"\n✓ Done! Master file: {combined_file_path}")

if __name__ == "__main__":
    # Since your script is IN the folder:
    main_folder = "./"
    output_folder = "./cleaned_output"
    process_files(main_folder, output_folder)