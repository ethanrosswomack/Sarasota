#!/usr/bin/env python3
"""
Intelligent PDF extraction for Voyagers volumes
Handles hyphenation rejoining, paragraph reflow, and chapter detection
"""

import pymupdf
import re
import os
from pathlib import Path

def clean_text_line(text):
    """Clean up common PDF artifacts from a line"""
    # Remove watermark
    if 'This PDF sold to' in text or 'dudeinwrens@gmail.com' in text or 'Transaction:' in text:
        return ''
    return text

def rejoin_hyphenated_words(lines):
    """Rejoin words that were split across lines with hyphens"""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Check if line ends with hyphen (word continuation)
        if line.endswith('-') and i + 1 < len(lines):
            next_line = lines[i + 1].lstrip()
            # Get the next word (first word of next line)
            next_words = next_line.split()
            if next_words:
                # Remove hyphen and join with next word
                line = line[:-1] + next_words[0]
                # Keep the rest of the next line
                if len(next_words) > 1:
                    lines[i + 1] = ' '.join(next_words[1:])
                else:
                    i += 1  # Skip the next line as we've consumed it
        
        result.append(line)
        i += 1
    
    return result

def reflow_paragraphs(lines):
    """Reflow lines into proper paragraphs"""
    paragraphs = []
    current_para = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            paragraphs.append('')  # Preserve paragraph break
            continue
        
        # Check if this looks like a heading (short, capitalized, etc.)
        is_heading = (
            len(line) < 80 and
            (line.isupper() or line.istitle()) and
            not line.endswith('.')
        )
        
        # Check if line looks like a new paragraph (indented or after break)
        is_new_para = (
            len(current_para) == 0 or
            is_heading or
            line.startswith('    ') or  # Indented
            re.match(r'^\d+\.', line) or  # Numbered list
            re.match(r'^[A-Z][a-z]+,', line)  # Starts with capitalized word + comma
        )
        
        if is_new_para and current_para:
            paragraphs.append(' '.join(current_para))
            current_para = []
        
        current_para.append(line)
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    return paragraphs

def extract_volume_1(pdf_path, output_dir):
    """Extract Volume 1 using TOC"""
    print(f"\nExtracting Volume 1 from {pdf_path}...")
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()
    
    # Group chapters
    chapters = []
    current_chapter = None
    
    for level, title, page in toc:
        if 'Chapter' in title and ':' in title:
            if current_chapter:
                chapters.append(current_chapter)
            current_chapter = {
                'title': title,
                'start_page': page,
                'content': []
            }
        elif current_chapter and level == 1:
            # Subheading within chapter
            current_chapter['content'].append(f"## {title}\n\n")
    
    if current_chapter:
        chapters.append(current_chapter)
    
    # Extract text for each chapter
    output_path = Path(output_dir) / 'voyagers_1'
    output_path.mkdir(parents=True, exist_ok=True)
    
    for i, chapter in enumerate(chapters):
        # Determine end page
        if i + 1 < len(chapters):
            end_page = chapters[i + 1]['start_page'] - 1
        else:
            end_page = len(doc)
        
        # Extract text
        full_text = []
        for page_num in range(chapter['start_page'] - 1, min(end_page, len(doc))):
            page = doc[page_num]
            text = page.get_text()
            lines = text.split('\n')
            lines = [clean_text_line(line) for line in lines if clean_text_line(line)]
            full_text.extend(lines)
        
        # Process text
        full_text = rejoin_hyphenated_words(full_text)
        paragraphs = reflow_paragraphs(full_text)
        
        # Create chapter file
        chapter_num = i + 1
        filename = f"chapter_{chapter_num}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write heading
            title_clean = chapter['title'].split(':')[0].strip()
            f.write(f"# {title_clean}\n\n")
            
            # Write content
            for para in paragraphs:
                if para:
                    f.write(para + '\n\n')
        
        print(f"  ✓ Extracted {filename}")
    
    doc.close()
    print(f"Volume 1: Extracted {len(chapters)} chapters")

def find_chapter_boundaries_vol2(doc):
    """Find chapter boundaries in Volume 2 by looking for chapter headings"""
    chapters = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        
        for line in lines[:10]:  # Check first 10 lines of each page
            # Look for chapter patterns
            match = re.match(r'^\s*(\d+)\s+(.*?)\.+\s*\d+\s*$', line)
            if match:
                chapter_num = int(match.group(1))
                chapter_title = match.group(2).strip()
                chapters.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'page': page_num + 1
                })
            # Also look for direct chapter headings
            elif re.match(r'^\s*Chapter\s+\d+', line, re.IGNORECASE):
                chapters.append({
                    'number': len(chapters) + 1,
                    'title': line.strip(),
                    'page': page_num + 1
                })
    
    return chapters

def extract_volume_2(pdf_path, output_dir):
    """Extract Volume 2 by finding chapter boundaries in text"""
    print(f"\nExtracting Volume 2 from {pdf_path}...")
    doc = pymupdf.open(pdf_path)
    
    # For now, use the existing markdown files as a guide for chapter count
    # but extract clean text from the PDF
    # We know there are 21 chapters + appendices
    
    # Simple approach: divide the book into sections based on page ranges
    # This is a starting point - we can refine based on actual chapter markers
    
    output_path = Path(output_dir) / 'voyagers_vol2'
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Extract full book text first
    print("  Extracting full text...")
    all_text = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')
        lines = [clean_text_line(line) for line in lines if clean_text_line(line)]
        all_text.extend(lines)
    
    # Rejoin hyphenated words
    print("  Rejoining hyphenated words...")
    all_text = rejoin_hyphenated_words(all_text)
    
    # Reflow paragraphs
    print("  Reflowing paragraphs...")
    paragraphs = reflow_paragraphs(all_text)
    
    # Save as single file for now (we can split later based on chapter markers)
    full_content_path = output_path / 'full_text.md'
    with open(full_content_path, 'w', encoding='utf-8') as f:
        f.write('# Voyagers Volume II: The Secrets of Amenti\n\n')
        for para in paragraphs[:5000]:  # First 5000 paragraphs to test
            if para:
                f.write(para + '\n\n')
    
    print(f"  ✓ Extracted full text to full_text.md")
    
    doc.close()
    print(f"Volume 2: Extracted as single file (will split into chapters next)")

if __name__ == '__main__':
    extract_volume_1('/tmp/voyagers_vol1.pdf', 'source_extracted')
    extract_volume_2('/tmp/voyagers_vol2.pdf', 'source_extracted')
    print("\n✅ Extraction complete!")
