# Sarasota Synchrony - Voyagers Restoration Codex

## Overview
This is a Sphinx-based static documentation website hosting the **Voyagers Restoration Codex 2025**. The site contains the digitally restored Voyagers transmissions archive, aligned with the EverLight Codex Archive and anchored near the original ARhAyas site in Sarasota, Florida.

## Project Type
Static documentation site built with Sphinx, using the Furo theme for a modern documentation experience.

## Current State
The project has been successfully set up in the Replit environment and is running on port 5000. The static site is served from the pre-built `build/html` directory using Python's built-in HTTP server.

## Architecture

### Build System
- **Sphinx**: Documentation generator that converts source files (Markdown and reStructuredText) into static HTML
- **Source Directory**: `source/` - Contains all documentation source files
- **Build Directory**: `build/html/` - Contains the generated static HTML files
- **Configuration**: `source/conf.py` - Sphinx configuration file

### Dependencies
- Python 3.11
- sphinx - Documentation builder
- myst-parser - Markdown parser for Sphinx
- furo - Modern Sphinx theme

### Content Structure
- **Voyagers Volume I**: Located in `source/voyagers_1/`
- **Voyagers Volume II**: Organized chapters in `source/voyagers_vol2/`
  - 21 individual chapter files (chapter_1.md through chapter_21.md)
  - Appendices with reference material
- **Frontmatter**: Introduction and archival information
- **Theme**: Furo with custom light/dark logos
- **Excluded**: The `voyagers_2/` directory (201 fragmented files) is excluded from the build

### AI Chatbot System
- **Backend**: Flask API running on port 8080 (`chatbot_api.py`)
- **RAG System**: Paragraph-level semantic search across all 21 chapters of Volume II
- **OpenAI Integration**: Uses Replit AI Integrations (gpt-4o-mini model)
- **Frontend**: Beautiful purple/green themed chat widget (`chatbot-widget.js`)
- **Features**: 
  - Contextual answers with chapter citations
  - Intelligent paragraph-level content retrieval
  - Production-ready with security hardening
  - Mobile-responsive chat interface

### Enhanced Features
- **Reading Progress Tracking**: LocalStorage-based progress tracking remembers last page visited
- **Continue Reading Button**: Homepage button to resume from last chapter
- **Mobile Responsive**: Full mobile optimization with touch-friendly controls
- **Built-in Search**: Sphinx search functionality for quick content lookup

### Deployment
- **Development**: Dual-workflow architecture
  - Static server on port 5000 (documentation site)
  - Chatbot API on port 8080 (AI assistant backend)
- **Production**: Configured for autoscale deployment with both services
- **External**: Also deployed to GitHub Pages at https://ethanrosswomack.github.io/Sarasota

## Running the Project

### Development Server
Two workflows run automatically:

**Server Workflow** (port 5000):
```bash
cd build/html && python -m http.server 5000 --bind 0.0.0.0
```

**Chatbot API Workflow** (port 8080):
```bash
python chatbot_api.py
```

### Rebuilding Documentation
If you need to rebuild the Sphinx documentation from source:
```bash
make html
```

## Important Notes
- The site is already built and ready to serve from `build/html`
- The `voyagers_2/` directory fragments are excluded from the build to avoid orphan pages
- The project uses MyST parser to support both Markdown and reStructuredText
- External links open in new tabs by default
- Base URL is set to https://sphinxguardian.com/

## Recent Changes
- 2025-10-30: AI CHATBOT SYSTEM - Production-ready AI assistant with RAG
  - **Flask backend API** with OpenAI integration (gpt-4o-mini via Replit AI Integrations)
  - **Paragraph-level RAG system** indexes all 21 chapters with intelligent semantic search
  - **Beautiful chat widget** with purple/green theme matching site aesthetic
  - **Production security hardening** (debug mode disabled, proper error handling)
  - **Tested and verified**: Accurate answers with proper chapter citations
  - **Reading progress tracking** with localStorage and "Continue Reading" button
  - **Mobile responsive enhancements** for touch devices
  - Architect-reviewed and approved for production deployment

- 2025-10-30: MAJOR REBUILD - Clean PDF extraction and custom mystical theme
  - **Extracted clean text directly from PDFs** using PyMuPDF with intelligent processing
  - Fixed hyphenation issues (no more "dimen-sional" breaks)
  - Proper paragraph reflow for smooth, readable prose
  - **Custom dark purple/green theme** with mystical aesthetic:
    - Dark purple backgrounds (#1a0f2e, #2a1b3d)
    - Green accents and headings (#7cd992, #9fe6ad)
    - Subtle glow effects on headings
    - Animated gradient background
    - Custom scrollbars and hover effects
  - **PDF download links** on homepage for both volumes
  - Volume 2: 21 chapters extracted with proper boundaries
  - All changes verified via screenshots
  
- 2025-10-30: Initial cleanup attempts (superseded by PDF extraction)
  - Removed Table of Contents headers from all chapters
  - Removed PDF watermarks and transaction information
  - Created cleaning scripts (later replaced by direct PDF extraction)
  
- 2025-10-29: Initial Replit environment setup completed
  - Installed Python 3.11 and required Sphinx dependencies
  - Configured workflow to serve static site on port 5000
  - Set up autoscale deployment configuration
  - Verified site is working correctly with Furo theme
