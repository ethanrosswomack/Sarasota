/**
 * Voyagers Reading Progress Tracker
 * Remembers last visited page and provides continue reading functionality
 */

(function() {
  'use strict';

  const STORAGE_KEY = 'voyagers_last_page';
  const STORAGE_TITLE_KEY = 'voyagers_last_title';
  const STORAGE_TIMESTAMP_KEY = 'voyagers_last_timestamp';

  /**
   * Save current page to localStorage
   */
  function saveProgress() {
    const currentPath = window.location.pathname;
    const currentTitle = document.title;
    const timestamp = new Date().toISOString();
    
    // Only save if we're on a chapter page (not homepage or search)
    if (currentPath.includes('chapter_') || currentPath.includes('voyagers')) {
      try {
        localStorage.setItem(STORAGE_KEY, currentPath);
        localStorage.setItem(STORAGE_TITLE_KEY, currentTitle);
        localStorage.setItem(STORAGE_TIMESTAMP_KEY, timestamp);
      } catch (e) {
        console.warn('Could not save reading progress:', e);
      }
    }
  }

  /**
   * Get last visited page from localStorage
   */
  function getLastPage() {
    try {
      return {
        path: localStorage.getItem(STORAGE_KEY),
        title: localStorage.getItem(STORAGE_TITLE_KEY),
        timestamp: localStorage.getItem(STORAGE_TIMESTAMP_KEY)
      };
    } catch (e) {
      console.warn('Could not retrieve reading progress:', e);
      return null;
    }
  }

  /**
   * Add continue reading button to homepage
   */
  function addContinueReading() {
    const lastPage = getLastPage();
    
    // Only show on homepage
    if (!window.location.pathname.endsWith('/') && 
        !window.location.pathname.endsWith('index.html')) {
      return;
    }
    
    if (!lastPage || !lastPage.path) {
      return;
    }

    // Find the download section to insert after
    const downloadSection = document.querySelector('.pdf-download')?.parentElement?.parentElement;
    
    if (downloadSection) {
      const continueDiv = document.createElement('div');
      continueDiv.style.cssText = `
        margin: 2em 0;
        padding: 1.5em 2em;
        background: linear-gradient(135deg, rgba(92, 201, 120, 0.15), rgba(126, 217, 146, 0.1));
        border-radius: 12px;
        border: 1px solid rgba(126, 217, 146, 0.3);
        border-left: 4px solid #7cd992;
      `;
      
      const title = lastPage.title.replace(' — Voyagers Restoration Codex 2025 documentation', '');
      const timeAgo = getTimeAgo(lastPage.timestamp);
      
      continueDiv.innerHTML = `
        <h3 style="color: #9fe6ad; margin-top: 0; margin-bottom: 0.5em;">
          📖 Continue Reading
        </h3>
        <p style="color: #c5b8d9; margin-bottom: 1em; font-size: 0.95em;">
          Last visited ${timeAgo}
        </p>
        <p style="color: #e8dff5; margin-bottom: 1.2em; font-weight: 500;">
          ${title}
        </p>
        <a href="${lastPage.path}" 
           style="display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #7cd992, #5bc978); 
                  color: #1a0f2e; text-decoration: none; border-radius: 6px; font-weight: 600; 
                  transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(92, 201, 120, 0.3);"
           onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 20px rgba(92, 201, 120, 0.5)';"
           onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 15px rgba(92, 201, 120, 0.3)';">
          Continue Reading →
        </a>
      `;
      
      downloadSection.parentNode.insertBefore(continueDiv, downloadSection.nextSibling);
    }
  }

  /**
   * Convert timestamp to human-readable time ago
   */
  function getTimeAgo(timestamp) {
    if (!timestamp) return 'recently';
    
    const now = new Date();
    const then = new Date(timestamp);
    const seconds = Math.floor((now - then) / 1000);
    
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
    return `on ${then.toLocaleDateString()}`;
  }

  /**
   * Add visual indicator for current progress in sidebar
   */
  function highlightProgress() {
    const lastPage = getLastPage();
    if (!lastPage || !lastPage.path) return;
    
    // Find the link in sidebar that matches last visited page
    const sidebarLinks = document.querySelectorAll('.sidebar-tree a.reference');
    sidebarLinks.forEach(link => {
      if (link.getAttribute('href') === lastPage.path) {
        // Add a subtle indicator
        const indicator = document.createElement('span');
        indicator.textContent = ' 📍';
        indicator.title = 'Last visited';
        indicator.style.opacity = '0.6';
        link.appendChild(indicator);
      }
    });
  }

  /**
   * Initialize on page load
   */
  function init() {
    // Save progress when user visits a page
    saveProgress();
    
    // Add continue reading button on homepage
    addContinueReading();
    
    // Highlight last visited in sidebar
    highlightProgress();
    
    // Update progress periodically while reading
    setInterval(saveProgress, 30000); // Every 30 seconds
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
