#!/usr/bin/env python3
"""
Extract clean text directly from PDF with smart layout preservation
"""

import fitz  # PyMuPDF
import re
from pathlib import Path

def clean_hyphenation(text):
    """Remove hyphenation artifacts"""
    # Pattern 1: word- \nword or word-\nword
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    # Pattern 2: word- word (hyphen with space, same line)
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    return text

def extract_vol2_by_toc(pdf_path, output_dir):
    """Extract Volume 2 using the TOC we found earlier"""
    doc = fitz.open(pdf_path)
    
    # Volume 2 chapter information (from our earlier analysis)
    # Page numbers where chapters likely start
    chapters = [
        {"num": 1, "title": "The Secrets of Amenti", "start_page": 12},
        {"num": 2, "title": "The Second Seeding", "start_page": 40},
        {"num": 3, "title": "The Third Seeding", "start_page": 63},
        {"num": 4, "title": "A Journey Toward Awakening", "start_page": 84},
        {"num": 5, "title": "Return to Amenti", "start_page": 100},
        {"num": 6, "title": "Ascension Mechanics", "start_page": 119},
        {"num": 7, "title": "Countdown to Amenti", "start_page": 135},
        {"num": 8, "title": "Current Events", "start_page": 155},
        {"num": 9, "title": "Time Shift", "start_page": 173},
        {"num": 10, "title": "Opening the Halls of Amenti", "start_page": 198},
        {"num": 11, "title": "Things to Come", "start_page": 212},
        {"num": 12, "title": "Author's Closing Statement", "start_page": 247},
        {"num": 13, "title": "Emergency Release GA", "start_page": 254},
        {"num": 14, "title": "Angelic Human Heritage & Rainbow Roundtables", "start_page": 274},
        {"num": 15, "title": "The Atlantian Conspiracy and Roundtables", "start_page": 323},
        {"num": 16, "title": "The 9/11/2001 Attack & the Illuminati OWO", "start_page": 348},
        {"num": 17, "title": "The Phi-Ex Wormhole & Illuminati OWO", "start_page": 367},
        {"num": 18, "title": "The Hidden Game-board Final Conflict Drama", "start_page": 379},
        {"num": 19, "title": "Master Templar Mechanics", "start_page": 394},
        {"num": 20, "title": "Forbidden Meetings and the Amenti Mission Continues", "start_page": 416},
        {"num": 21, "title": "2012 Cont'd—The Secrets of Amenti Exposed", "start_page": 435},
    ]
    
    output_path = Path(output_dir) / 'voyagers_vol2'
    output_path.mkdir(parents=True, exist_ok=True)
    
    for i, chapter in enumerate(chapters):
        start = chapter['start_page']
        end = chapters[i+1]['start_page'] if i+1 < len(chapters) else len(doc)
        
        print(f"Extracting Chapter {chapter['num']}: {chapter['title']} (pages {start}-{end})...")
        
        # Extract text using layout-preserving mode
        chapter_text = ""
        for page_num in range(start, min(end, len(doc))):
            page = doc[page_num]
            # Use dict mode for better layout preservation
            blocks = page.get_text("dict")["blocks"]
            page_text = ""
            for block in blocks:
                if block['type'] == 0:  # Text block
                    for line in block['lines']:
                        line_text = ""
                        for span in line['spans']:
                            line_text += span['text']
                        page_text += line_text + "\n"
            chapter_text += page_text + "\n"
        
        # Clean watermarks
        chapter_text = re.sub(r'This PDF sold to.*?Transaction:.*?\d+', '', chapter_text, flags=re.DOTALL)
        
        # Fix hyphenation
        chapter_text = clean_hyphenation(chapter_text)
        
        # Write chapter
        filename = f"chapter_{chapter['num']}.md"
        with open(output_path / filename, 'w', encoding='utf-8') as f:
            f.write(f"# Chapter {chapter['num']}: {chapter['title']}\n\n")
            f.write(chapter_text)
        
        print(f"  ✓ {filename}")
    
    doc.close()
    print(f"\n✅ Extracted {len(chapters)} chapters")

if __name__ == '__main__':
    extract_vol2_by_toc('/tmp/voyagers_vol2.pdf', 'source')
    print("✅ Extraction complete!")
