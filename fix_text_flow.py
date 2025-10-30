#!/usr/bin/env python3
"""
Fix text flow in existing markdown files
- Rejoin hyphenated words
- Reflow paragraphs
- Clean formatting
"""

import re
import glob
from pathlib import Path

def fix_hyphenation_and_reflow(content):
    """Fix hyphenated words and reflow text"""
    lines = content.split('\n')
    fixed_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Preserve heading lines
        if line.startswith('#'):
            fixed_lines.append(line)
            i += 1
            continue
        
        # Check if line ends with hyphen and next line continues the word
        if i + 1 < len(lines) and line.rstrip().endswith('-'):
            next_line = lines[i + 1]
            # If next line starts with lowercase, it's likely a continuation
            if next_line and next_line[0].islower():
                # Remove hyphen and join
                line = line.rstrip()[:-1] + next_line.lstrip()
                i += 2
                fixed_lines.append(line)
                continue
        
        fixed_lines.append(line)
        i += 1
    
    # Now reflow paragraphs
    result = []
    current_para = []
    
    for line in fixed_lines:
        stripped = line.strip()
        
        # Preserve headings and empty lines
        if line.startswith('#') or not stripped:
            if current_para:
                # Join current paragraph
                result.append(' '.join(current_para))
                current_para = []
            result.append(line)
            continue
        
        # Check if this looks like a new paragraph start
        # (indentation, list, or after blank line)
        is_new_para = (
            len(current_para) == 0 or
            stripped[0].isupper() and len(current_para) > 5 or  # New sentence after enough text
            re.match(r'^\d+\.', stripped)  # Numbered list
        )
        
        # For Volume 2 with its formatting issues, be more aggressive about joining
        # Most line breaks are artificial from PDF layout
        if not is_new_para or len(current_para) < 3:
            current_para.append(stripped)
        else:
            if current_para:
                result.append(' '.join(current_para))
            current_para = [stripped]
    
    if current_para:
        result.append(' '.join(current_para))
    
    return '\n\n'.join(result)

def process_directory(input_dir, output_dir):
    """Process all markdown files in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    md_files = list(input_path.glob('*.md'))
    print(f"Processing {len(md_files)} files from {input_dir}...")
    
    for filepath in sorted(md_files):
        print(f"  Processing {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix text flow
        fixed_content = fix_hyphenation_and_reflow(content)
        
        # Write to output
        output_file = output_path / filepath.name
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"    ✓ Fixed")
    
    print(f"✅ Processed {len(md_files)} files")

if __name__ == '__main__':
    # Fix Volume 2 files
    process_directory('source/voyagers_vol2', 'source/voyagers_vol2_fixed')
    print(f"\n✅ All files processed!")
