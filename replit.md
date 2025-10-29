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
- **Voyagers Volume II**: Single chaptered document at `source/Voyagers_2_chaptered.md`
- **Frontmatter**: Introduction and archival information
- **Theme**: Furo with custom light/dark logos

### Deployment
- **Development**: Python HTTP server on port 5000, bound to 0.0.0.0
- **Production**: Configured for autoscale deployment
- **External**: Also deployed to GitHub Pages at https://ethanrosswomack.github.io/Sarasota

## Running the Project

### Development Server
The workflow "Server" runs automatically and serves the site on port 5000:
```bash
cd build/html && python -m http.server 5000 --bind 0.0.0.0
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
- 2025-10-29: Initial Replit environment setup completed
  - Installed Python 3.11 and required Sphinx dependencies
  - Configured workflow to serve static site on port 5000
  - Set up autoscale deployment configuration
  - Verified site is working correctly with Furo theme
