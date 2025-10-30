#!/usr/bin/env python3
"""
Aggressively clean Voyagers Volume 2 chapter files
Remove all Table of Contents and formatting artifacts
"""

import re
import glob
import os

def clean_chapter_aggressive(content, filename):
    """Aggressively clean a chapter file"""
    
    lines = content.split('\n')
    
    # Find the chapter heading
    chapter_heading = None
    for i, line in enumerate(lines):
        if line.strip().startswith('# Chapter') or line.strip().startswith('# Appendices'):
            chapter_heading = line
            break
    
    if not chapter_heading:
        return content  # Can't process if no heading found
    
    # For Chapter 1, we need to skip the entire TOC section
    # Look for where actual narrative content begins
    cleaned_lines = [chapter_heading, ""]
    
    in_toc = True
    found_content = False
    consecutive_blank = 0
    
    for i, line in enumerate(lines):
        # Skip the heading line (already added)
        if line.strip().startswith('# Chapter') or line.strip().startswith('# Appendices'):
            continue
        
        # Remove PDF watermarks
        if 'This PDF sold to' in line or 'dudeinwrens@gmail.com' in line or 'Transaction:' in line:
            continue
        
        # Remove "ORIGINAL MATERIAL", "Table of Contents", etc.
        if any(x in line for x in ['ORIGINAL MATERIAL', 'Table of Contents', '2001 UPDATE SECTION']):
            continue
        
        # Skip TOC-style lines (dots followed by page numbers)
        if re.search(r'\.{3,}\s*\d+', line):
            continue
        
        # Skip lines that are mostly dots/spaces
        if re.match(r'^[\s\.]+$', line):
            continue
        
        # Skip standalone page numbers and roman numerals
        if re.match(r'^\s*\d{1,4}\s*$', line) or re.match(r'^\s*[ivxlcdm]{1,10}\s*$', line, re.IGNORECASE):
            continue
        
        # Skip underscores (separator lines)
        if re.match(r'^\s*_{3,}\s*$', line):
            continue
        
        # Track consecutive blank lines
        if not line.strip():
            consecutive_blank += 1
            if consecutive_blank > 2:
                continue  # Skip excessive blanks
            if found_content:
                cleaned_lines.append(line)
            continue
        else:
            consecutive_blank = 0
        
        # Check if this looks like actual narrative content
        # (paragraph text, not TOC entries)
        if not in_toc or (len(line.strip()) > 40 and not re.search(r'\.{3,}', line)):
            in_toc = False
            found_content = True
            cleaned_lines.append(line)
    
    # If we didn't find narrative content, add a note
    if not found_content or len(cleaned_lines) < 10:
        cleaned_lines = [
            chapter_heading,
            "",
            "*[This chapter excerpt begins mid-content from the original PDF. Some introductory material may be missing.]*",
            ""
        ] + cleaned_lines[2:]
    
    result = '\n'.join(cleaned_lines)
    
    # Clean up excessive whitespace
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    return result.strip() + '\n'

def process_directory(directory):
    """Process all markdown files"""
    
    pattern = os.path.join(directory, '*.md')
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} files to clean")
    
    for filepath in sorted(files):
        filename = os.path.basename(filepath)
        print(f"Cleaning {filename}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned = clean_chapter_aggressive(content, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned)
            
            print(f"  ✓ Done")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == '__main__':
    process_directory('source/voyagers_vol2')
    print("\n✅ Aggressive cleaning complete!")
