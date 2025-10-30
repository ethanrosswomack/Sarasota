#!/usr/bin/env python3
"""
Voyagers AI Chatbot API
Uses OpenAI to answer questions about Voyagers content with RAG
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import json
from openai import OpenAI
import re

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with Replit AI Integrations
client = OpenAI(
    api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
    base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL")
)

# Simple in-memory index of Voyagers content
voyagers_index = {}

def load_voyagers_content():
    """Load and index all Voyagers content"""
    global voyagers_index
    
    print("Loading Voyagers content...")
    content_dirs = [
        Path("source/voyagers_vol2"),
        # Path("source/voyagers_1")  # Add Vol 1 later
    ]
    
    for content_dir in content_dirs:
        if not content_dir.exists():
            continue
            
        for md_file in content_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract chapter number and title
            chapter_match = re.search(r'# Chapter (\d+):?\s*(.+)?', content)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2) or f"Chapter {chapter_num}"
                
                # Split into chunks (paragraphs)
                paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
                
                volume = "Volume II" if "vol2" in str(content_dir) else "Volume I"
                
                voyagers_index[f"{volume}_ch{chapter_num}"] = {
                    "volume": volume,
                    "chapter": chapter_num,
                    "title": chapter_title,
                    "content": content,
                    "paragraphs": paragraphs[:100]  # Limit to first 100 paragraphs
                }
    
    print(f"Loaded {len(voyagers_index)} chapters")

def search_relevant_content(query, top_k=3):
    """Simple keyword-based search for relevant content"""
    query_lower = query.lower()
    query_terms = set(re.findall(r'\w+', query_lower))
    
    # Score each chapter
    scores = []
    for key, data in voyagers_index.items():
        content_lower = data['content'].lower()
        
        # Simple scoring: count matching terms
        matches = sum(1 for term in query_terms if term in content_lower)
        
        # Boost if query appears as phrase
        if query_lower in content_lower:
            matches += 10
        
        if matches > 0:
            scores.append((matches, key, data))
    
    # Sort by score and return top k
    scores.sort(reverse=True)
    return [
        {
            "volume": data["volume"],
            "chapter": data["chapter"],
            "title": data["title"],
            "relevant_text": "\n\n".join(data["paragraphs"][:5])  # First 5 paragraphs
        }
        for score, key, data in scores[:top_k]
    ]

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    # Search for relevant content
    relevant_docs = search_relevant_content(user_message, top_k=2)
    
    # Build context from relevant documents
    context = "\n\n---\n\n".join([
        f"From {doc['volume']}, Chapter {doc['chapter']}: {doc['title']}\n\n{doc['relevant_text']}"
        for doc in relevant_docs
    ])
    
    # Create system prompt
    system_prompt = f"""You are a knowledgeable assistant for the Voyagers books by Ashayana Deane, which contain information about the Guardian Alliance, Keylontic Science, human origins, and the Amenti rescue mission.

Your role is to:
1. Answer questions accurately based on the Voyagers content provided
2. Cite which volume and chapter your information comes from
3. Be clear when you're uncertain or when information isn't in the provided context
4. Maintain the mystical and educational tone of the source material

When answering:
- Reference specific chapters and volumes when possible
- Use terminology from the books (like "Sphere of Amenti", "Guardian Alliance", "morphogenetic field", etc.)
- Be respectful of the material's spiritual nature
- Admit when information is not in the provided context

Here is the relevant content from the Voyagers books:

{context if context else "No specific relevant content found. Answer based on general knowledge of the Voyagers material."}"""

    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using mini for efficiency
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        assistant_message = response.choices[0].message.content
        
        return jsonify({
            "response": assistant_message,
            "sources": [
                {
                    "volume": doc["volume"],
                    "chapter": doc["chapter"],
                    "title": doc["title"]
                }
                for doc in relevant_docs
            ]
        })
        
    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "indexed_chapters": len(voyagers_index)
    })

if __name__ == '__main__':
    # Load content on startup
    load_voyagers_content()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
