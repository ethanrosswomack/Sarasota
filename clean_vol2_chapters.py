#!/usr/bin/env python3
"""
Clean Voyagers Volume 2 chapter files by removing headers, footers, and artifacts
"""

import re
import glob
import os

def clean_chapter(content):
    """Clean a single chapter's content"""
    
    lines = content.split('\n')
    cleaned_lines = []
    found_content_start = False
    skip_next_blank_lines = False
    
    for i, line in enumerate(lines):
        # Keep the chapter heading
        if line.strip().startswith('# Chapter') or line.strip().startswith('# Appendices'):
            cleaned_lines.append(line)
            skip_next_blank_lines = True
            continue
        
        # Remove PDF watermarks
        if 'This PDF sold to' in line or 'dudeinwrens@gmail.com' in line or 'Transaction:' in line:
            continue
        
        # Remove "Table of Contents" headers
        if 'Table of Contents' in line:
            continue
            
        # Remove lines that are mostly dots/spaces (TOC formatting)
        if re.match(r'^[\s\.]+[ivx\d]+\s*$', line) or re.match(r'^[\s\.]+\d+\s*$', line):
            continue
        
        # Remove "Preface to Volume" references
        if 'Preface to Volume' in line or 'Required Reading' in line:
            continue
            
        # Remove standalone page numbers
        if re.match(r'^\s*\d{1,3}\s*$', line):
            continue
        
        # Remove lines that are just roman numerals
        if re.match(r'^\s*[ivxlcdm]+\s*$', line, re.IGNORECASE) and len(line.strip()) < 10:
            continue
        
        # Skip excessive blank lines at start
        if skip_next_blank_lines and not line.strip():
            continue
        elif skip_next_blank_lines and line.strip():
            skip_next_blank_lines = False
            found_content_start = True
        
        # After finding content start, keep everything except watermarks
        if found_content_start or (line.strip() and not skip_next_blank_lines):
            found_content_start = True
            cleaned_lines.append(line)
    
    # Join lines and clean up excessive whitespace
    result = '\n'.join(cleaned_lines)
    
    # Remove excessive blank lines (more than 2 consecutive)
    result = re.sub(r'\n{4,}', '\n\n\n', result)
    
    return result.strip() + '\n'

def process_directory(directory):
    """Process all markdown files in the directory"""
    
    pattern = os.path.join(directory, '*.md')
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} files to process in {directory}")
    
    for filepath in sorted(files):
        print(f"Processing {os.path.basename(filepath)}...")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            cleaned_content = clean_chapter(content)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"  ✓ Cleaned successfully")
            
        except Exception as e:
            print(f"  ✗ Error: {e}")

if __name__ == '__main__':
    process_directory('source/voyagers_vol2')
    print("\n✅ All files processed!")
