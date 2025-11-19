#!/usr/bin/env python3
"""
Voyagers AI Chatbot API
Uses OpenAI to answer questions about Voyagers content with RAG
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pathlib import Path
import re
from openai import OpenAI

# ------------------------------------------------------------------------------
# Flask app + OpenAI client setup
# ------------------------------------------------------------------------------

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client with Replit AI Integrations (or any OpenAI API base)
client = OpenAI(
    api_key=os.environ.get("AI_INTEGRATIONS_OPENAI_API_KEY"),
    base_url=os.environ.get("AI_INTEGRATIONS_OPENAI_BASE_URL"),
)

# Simple in-memory index of Voyagers content
voyagers_index = {}


# ------------------------------------------------------------------------------
# Index loading
# ------------------------------------------------------------------------------

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
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract chapter number and title
            chapter_match = re.search(r"# Chapter (\d+):?\s*(.+)?", content)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2) or f"Chapter {chapter_num}"

                # Split into chunks (paragraphs), skipping headings
                paragraphs = [
                    p.strip()
                    for p in content.split("\n\n")
                    if p.strip() and not p.startswith("#")
                ]

                volume = "Volume II" if "vol2" in str(content_dir) else "Volume I"

                voyagers_index[f"{volume}_ch{chapter_num}"] = {
                    "volume": volume,
                    "chapter": chapter_num,
                    "title": chapter_title,
                    "content": content,
                    "paragraphs": paragraphs[:100],
                }

    print(f"Loaded {len(voyagers_index)} chapters")


# 🔹 Load index once, when the module is imported
load_voyagers_content()


# ------------------------------------------------------------------------------
# Search
# ------------------------------------------------------------------------------

def search_relevant_content(query: str, top_k: int = 3):
    """Search for relevant paragraphs across all chapters"""
    query_lower = query.lower()
    query_terms = set(re.findall(r"\w+", query_lower))

    paragraph_scores = []

    for key, data in voyagers_index.items():
        for i, paragraph in enumerate(data["paragraphs"]):
            para_lower = paragraph.lower()

            term_matches = sum(1 for term in query_terms if term in para_lower)
            phrase_boost = 15 if query_lower in para_lower else 0

            score = term_matches + phrase_boost
            if score > 0:
                paragraph_scores.append(
                    {
                        "score": score,
                        "volume": data["volume"],
                        "chapter": data["chapter"],
                        "title": data["title"],
                        "paragraph": paragraph,
                        "para_index": i,
                    }
                )

    paragraph_scores.sort(key=lambda x: x["score"], reverse=True)

    # Group by chapter
    chapter_contexts = {}
    for para_data in paragraph_scores[:15]:  # Top 15 paragraphs
        chapter_key = f"{para_data['volume']}_ch{para_data['chapter']}"
        if chapter_key not in chapter_contexts:
            chapter_contexts[chapter_key] = {
                "volume": para_data["volume"],
                "chapter": para_data["chapter"],
                "title": para_data["title"],
                "paragraphs": [],
            }
        chapter_contexts[chapter_key]["paragraphs"].append(para_data["paragraph"])

    # Build results from top chapters
    results = []
    for chapter_key in list(chapter_contexts.keys())[:top_k]:
        chapter_data = chapter_contexts[chapter_key]
        results.append(
            {
                "volume": chapter_data["volume"],
                "chapter": chapter_data["chapter"],
                "title": chapter_data["title"],
                "relevant_text": "\n\n".join(
                    chapter_data["paragraphs"][:8]
                ),  # Top 8 relevant paragraphs
            }
        )

    return results


# ------------------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handle chat requests"""
    data = request.json or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Search for relevant content
    relevant_docs = search_relevant_content(user_message, top_k=2)

    # Build context from relevant documents
    context = "\n\n---\n\n".join(
        [
            f"From {doc['volume']}, Chapter {doc['chapter']}: {doc['title']}\n\n{doc['relevant_text']}"
            for doc in relevant_docs
        ]
    )

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

{context if context else "No specific relevant content found. Answer based on general knowledge of the Voyagers material."}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=800,
        )

        assistant_message = response.choices[0].message.content

        return jsonify(
            {
                "response": assistant_message,
                "sources": [
                    {
                        "volume": doc["volume"],
                        "chapter": doc["chapter"],
                        "title": doc["title"],
                    }
                    for doc in relevant_docs
                ],
            }
        )

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "indexed_chapters": len(voyagers_index),
        }
    )


# ------------------------------------------------------------------------------
# Local dev entrypoint
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
