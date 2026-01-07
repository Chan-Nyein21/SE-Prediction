/**
 * Year Selector - Manages admission year selection across all pages
 * Automatically generates years from 2020 to (current year + 1)
 * Persists selection using localStorage
 */

(function() {
    'use strict';

    // Configuration
    const START_YEAR = 2020;
    const STORAGE_KEY = 'selectedAdmissionYear';

    /**
     * Get current year and calculate max year (current + 1)
     */
    function getYearRange() {
        const currentYear = new Date().getFullYear();
        const maxYear = currentYear + 1;
        return { startYear: START_YEAR, maxYear: maxYear };
    }

    /**
     * Get stored year or default to current year + 1
     */
    function getSelectedYear() {
        const stored = localStorage.getItem(STORAGE_KEY);
        const { maxYear } = getYearRange();
        
        if (stored && parseInt(stored) >= START_YEAR) {
            return parseInt(stored);
        }
        return maxYear; // Default to next year
    }

    /**
     * Save selected year to localStorage
     */
    function saveSelectedYear(year) {
        localStorage.setItem(STORAGE_KEY, year.toString());
        // Also store in session for backend access
        sessionStorage.setItem(STORAGE_KEY, year.toString());
    }

    /**
     * Populate the year dropdown
     */
    function populateYearDropdown() {
        const select = document.getElementById('admissionYear');
        if (!select) return;

        const { startYear, maxYear } = getYearRange();
        const selectedYear = getSelectedYear();

        // Clear existing options
        select.innerHTML = '';

        // Add years in descending order (newest first)
        for (let year = maxYear; year >= startYear; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            
            if (year === selectedYear) {
                option.selected = true;
            }
            
            select.appendChild(option);
        }

        // Update hidden input if exists (for predict form)
        const hiddenInput = document.getElementById('selectedYear');
        if (hiddenInput) {
            hiddenInput.value = selectedYear;
        }
    }

    /**
     * Handle year change event
     */
    function handleYearChange(event) {
        const newYear = parseInt(event.target.value);
        saveSelectedYear(newYear);
        
        // Update hidden input if exists
        const hiddenInput = document.getElementById('selectedYear');
        if (hiddenInput) {
            hiddenInput.value = newYear;
        }

        // Show notification
        showYearChangeNotification(newYear);

        // Reload data for current page
        reloadPageData(newYear);
    }

    /**
     * Show year change notification
     */
    function showYearChangeNotification(year) {
        // Remove existing notifications
        const existing = document.querySelector('.year-notification');
        if (existing) existing.remove();

        // Create notification
        const notification = document.createElement('div');
        notification.className = 'year-notification';
        notification.innerHTML = `
            <i class="bi bi-check-circle-fill"></i>
            <span>Displaying data for admission year <strong>${year}</strong></span>
        `;
        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('show'), 10);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    /**
     * Reload page data based on selected year
     */
    function reloadPageData(year) {
        // This will be expanded to fetch data from backend based on year
        console.log(`Loading data for admission year: ${year}`);
        
        // For now, we'll reload the page to update with new year parameter
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('year', year);
        
        // Update URL without reloading (using History API)
        window.history.replaceState({ year: year }, '', currentUrl.toString());
        
        // In future implementation, make AJAX call to fetch year-specific data
        // Example:
        // fetch(`/api/data?year=${year}`)
        //     .then(response => response.json())
        //     .then(data => updatePageContent(data));
    }

    /**
     * Get year from URL parameter
     */
    function getYearFromURL() {
        const urlParams = new URLSearchParams(window.location.search);
        const yearParam = urlParams.get('year');
        if (yearParam) {
            const year = parseInt(yearParam);
            if (year >= START_YEAR) {
                return year;
            }
        }
        return null;
    }

    /**
     * Initialize year selector
     */
    function initYearSelector() {
        // Check if year selector exists on this page
        const select = document.getElementById('admissionYear');
        if (!select) return;

        // Check for year in URL (takes precedence)
        const urlYear = getYearFromURL();
        if (urlYear) {
            saveSelectedYear(urlYear);
        }

        // Populate dropdown
        populateYearDropdown();

        // Add change event listener
        select.addEventListener('change', handleYearChange);

        // Display current year in console for debugging
        console.log(`Admission Year Selector initialized. Current year: ${getSelectedYear()}`);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initYearSelector);
    } else {
        initYearSelector();
    }

    // Expose API for external use
    window.AdmissionYear = {
        get: getSelectedYear,
        set: saveSelectedYear,
        getRange: getYearRange
    };
})();
