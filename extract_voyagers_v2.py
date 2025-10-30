#!/usr/bin/env python3
"""
Improved PDF extraction for Voyagers volumes
"""

import pymupdf
import re
import os
from pathlib import Path

def clean_watermark(text):
    """Remove watermarks and transaction info"""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        if any(x in line for x in ['This PDF sold to', 'dudeinwrens@gmail.com', 'Transaction:']):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned)

def rejoin_hyphenated_words(text):
    """Rejoin words split across lines with hyphens"""
    # Replace "word-\nword" with "wordword"
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    return text

def reflow_paragraphs(text):
    """Reflow text into proper paragraphs"""
    # Remove single line breaks but keep double line breaks (paragraph separators)
    text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)
    return text

def extract_volume_1_full(pdf_path, output_dir):
    """Extract Volume 1 with full text per chapter"""
    print(f"\nExtracting Volume 1 from {pdf_path}...")
    doc = pymupdf.open(pdf_path)
    toc = doc.get_toc()
    
    # Find chapter entries in TOC
    chapter_entries = []
    for level, title, page in toc:
        if 'Chapter' in title and ':' in title:
            chapter_entries.append({
                'title': title,
                'page': page
            })
    
    output_path = Path(output_dir) / 'voyagers_1'
    output_path.mkdir(parents=True, exist_ok=True)
    
    for i, chapter in enumerate(chapter_entries):
        start_page = chapter['page'] - 1  # Convert to 0-indexed
        if i + 1 < len(chapter_entries):
            end_page = chapter_entries[i + 1]['page'] - 1
        else:
            end_page = len(doc)
        
        # Extract text from pages
        chapter_text = ""
        for page_num in range(start_page, min(end_page, len(doc))):
            page = doc[page_num]
            page_text = page.get_text()
            chapter_text += page_text + "\n"
        
        # Clean and process
        chapter_text = clean_watermark(chapter_text)
        chapter_text = rejoin_hyphenated_words(chapter_text)
        chapter_text = reflow_paragraphs(chapter_text)
        
        # Write to file
        chapter_num = i + 1
        filename = f"chapter_{chapter_num}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            title_parts = chapter['title'].split(':')
            chapter_name = title_parts[0].strip()
            f.write(f"# {chapter_name}\n\n")
            f.write(chapter_text)
        
        print(f"  ✓ {filename} ({end_page - start_page} pages)")
    
    doc.close()
    print(f"Volume 1: Extracted {len(chapter_entries)} chapters")
    return len(chapter_entries)

def split_vol2_into_chapters(full_text_path, output_dir):
    """Split Volume 2 full text into chapters based on chapter markers"""
    print(f"\nSplitting Volume 2 into chapters...")
    
    with open(full_text_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by chapter markers in the TOC we extracted
    # The pattern is: number followed by chapter title
    chapter_pattern = r'\n(\d+)\s+([^\n]{10,100}?)\s*\.{2,}\s*\d+\s*\n'
    
    matches = list(re.finditer(chapter_pattern, content))
    
    output_path = Path(output_dir) / 'voyagers_vol2'
    output_path.mkdir(parents=True, exist_ok=True)
    
    if not matches:
        print("  ⚠ No chapter markers found, using alternative method...")
        # Try alternative: look for "Chapter X" headers
        chapter_pattern2 = r'\n(Chapter\s+\d+)[^\n]*\n'
        matches = list(re.finditer(chapter_pattern2, content, re.IGNORECASE))
    
    # Extract chapters
    for i, match in enumerate(matches[:22]):  # 21 chapters + appendices
        start_pos = match.end()
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            end_pos = len(content)
        
        chapter_content = content[start_pos:end_pos].strip()
        
        # Get chapter number
        chapter_num_match = re.search(r'\d+', match.group(1))
        if chapter_num_match:
            chapter_num = chapter_num_match.group()
        else:
            chapter_num = i + 1
        
        filename = f"chapter_{chapter_num}.md"
        filepath = output_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Chapter {chapter_num}\n\n")
            f.write(chapter_content)
        
        print(f"  ✓ {filename}")
    
    print(f"Volume 2: Split into {min(len(matches), 22)} chapters")

def extract_volume_2_smart(pdf_path, output_dir):
    """Extract Volume 2 with intelligent chapter detection"""
    print(f"\nExtracting Volume 2 from {pdf_path}...")
    doc = pymupdf.open(pdf_path)
    
    # Strategy: Extract full text first, then split by chapter markers
    full_text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        page_text = page.get_text()
        full_text += page_text + "\n\n"
    
    # Clean
    full_text = clean_watermark(full_text)
    full_text = rejoin_hyphenated_words(full_text)
    # Don't reflow yet - we need to find chapter boundaries first
    
    # Find chapter start positions
    # Look for pattern like "1 The Secrets of Amenti.....1" in TOC
    # Then later "The Secrets of Amenti" as actual chapter start
    
    # Extract TOC section first
    toc_start = full_text.find('Table of Contents')
    toc_end = full_text.find('ORIGINAL MATERIAL', toc_start)
    
    if toc_start > 0 and toc_end > toc_start:
        toc_text = full_text[toc_start:toc_end]
        
        # Parse TOC entries
        chapter_pattern = r'(\d+)\s+(.+?)\.{2,}\s*(\d+)'
        chapters = []
        for match in re.finditer(chapter_pattern, toc_text):
            ch_num = match.group(1)
            ch_title = match.group(2).strip()
            chapters.append({
                'number': ch_num,
                'title': ch_title
            })
        
        print(f"  Found {len(chapters)} chapters in TOC")
        
        # Now find actual chapter content after TOC
        content_start = toc_end + 100  # Skip past "ORIGINAL MATERIAL"
        main_content = full_text[content_start:]
        
        output_path = Path(output_dir) / 'voyagers_vol2'
        output_path.mkdir(parents=True, exist_ok=True)
        
        # For each chapter title, find where it appears in the content
        for i, chapter in enumerate(chapters[:21]):  # First 21 are main chapters
            title = chapter['title']
            
            # Find this title in content
            title_pos = main_content.find(title)
            if title_pos < 0:
                # Try without special characters
                title_clean = re.sub(r'[^\w\s]', '', title)
                title_pos = main_content.find(title_clean)
            
            if title_pos >= 0:
                # Find next chapter
                if i + 1 < len(chapters):
                    next_title = chapters[i + 1]['title']
                    next_pos = main_content.find(next_title, title_pos + 100)
                    if next_pos < 0:
                        next_pos = len(main_content)
                else:
                    next_pos = len(main_content)
                
                # Extract chapter content
                chapter_text = main_content[title_pos:next_pos]
                chapter_text = reflow_paragraphs(chapter_text)
                
                # Save
                filename = f"chapter_{chapter['number']}.md"
                filepath = output_path / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# Chapter {chapter['number']}\n\n")
                    f.write(chapter_text.strip())
                
                print(f"  ✓ {filename}")
        
        print(f"Volume 2: Extracted {min(len(chapters), 21)} chapters")
    else:
        print("  ⚠ Could not find TOC, using fallback extraction")
    
    doc.close()

if __name__ == '__main__':
    extract_volume_1_full('/tmp/voyagers_vol1.pdf', 'source')
    extract_volume_2_smart('/tmp/voyagers_vol2.pdf', 'source')
    print("\n✅ Extraction complete!")
