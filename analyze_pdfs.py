#!/usr/bin/env python3
"""
Analyze PDF structure to understand chapter organization
"""

import pymupdf
import pdfplumber

def analyze_pdf(pdf_path, name):
    print(f"\n{'='*60}")
    print(f"Analyzing {name}")
    print(f"{'='*60}")
    
    # Using PyMuPDF for basic info
    doc = pymupdf.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    print(f"\nFirst 5 pages structure:")
    
    for page_num in range(min(5, len(doc))):
        page = doc[page_num]
        text = page.get_text()
        lines = text.split('\n')[:10]  # First 10 lines
        print(f"\n--- Page {page_num + 1} (first 10 lines) ---")
        for line in lines:
            if line.strip():
                print(f"  {line[:80]}")
    
    # Check TOC
    toc = doc.get_toc()
    if toc:
        print(f"\n\nTable of Contents ({len(toc)} entries):")
        for i, entry in enumerate(toc[:15]):  # First 15 TOC entries
            level, title, page = entry
            print(f"  {'  ' * (level-1)}{title} (page {page})")
    else:
        print("\nNo embedded TOC found")
    
    doc.close()
    
    # Sample text extraction with pdfplumber
    print(f"\n\nSample text extraction (page 10):")
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) >= 10:
            page = pdf.pages[9]  # Page 10
            text = page.extract_text()
            print(text[:500])

if __name__ == '__main__':
    analyze_pdf('/tmp/voyagers_vol1.pdf', 'Volume 1')
    analyze_pdf('/tmp/voyagers_vol2.pdf', 'Volume 2')
