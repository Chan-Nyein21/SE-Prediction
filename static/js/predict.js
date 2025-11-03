// File Upload Handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileName = document.getElementById('fileName');
    const predictForm = document.getElementById('predictForm');
    const predictBtn = document.getElementById('predictBtn');
    const resultCard = document.getElementById('resultCard');
    const emptyState = document.getElementById('emptyState');
    
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // File selected
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            fileName.textContent = `Selected: ${file.name}`;
            predictBtn.disabled = false;
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            fileName.textContent = `Selected: ${file.name}`;
            predictBtn.disabled = false;
        }
    });
    
    // Form submission (for demo - will show result)
    predictForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Show loading state
        predictBtn.textContent = 'Predicting...';
        predictBtn.disabled = true;
        
        // Simulate prediction (in real app, this would be an API call)
        setTimeout(() => {
            // Hide empty state and show result
            emptyState.style.display = 'none';
            resultCard.style.display = 'block';
            
            // Reset button
            predictBtn.textContent = 'Predict';
            predictBtn.disabled = false;
            
            // Scroll to result
            resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 2000);
    });
});
