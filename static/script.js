// State Management
let uploadedFiles = [];
let extractedResults = [];
let currentSessionId = null;
let currentPageIndex = 0;
let currentFileIndex = 0;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    document.getElementById('currentYear').textContent = new Date().getFullYear();
});

// Event Listeners
function initializeEventListeners() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    uploadArea.addEventListener('click', () => fileInput.click());

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').style.backgroundColor = 'rgba(102, 126, 234, 0.15)';
    document.getElementById('uploadArea').style.borderColor = '#764ba2';
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').style.backgroundColor = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
    document.getElementById('uploadArea').style.borderColor = '#667eea';
}

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('uploadArea').style.backgroundColor = 'linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%)';
    document.getElementById('uploadArea').style.borderColor = '#667eea';
    
    handleFiles(e.dataTransfer.files);
}

// Handle Files
function handleFiles(files) {
    const newFiles = Array.from(files);
    uploadedFiles = uploadedFiles.concat(newFiles);
    updateFilesList();
    showStatus('Files added successfully!', 'success');
}

// Update Files List
function updateFilesList() {
    const filesList = document.getElementById('filesList');
    
    if (uploadedFiles.length === 0) {
        filesList.innerHTML = '<div class="empty-state"><p>No files selected yet</p></div>';
        document.getElementById('fileCount').textContent = '0 files';
        return;
    }

    filesList.innerHTML = uploadedFiles.map((file, index) => `
        <div class="file-item">
            <div class="file-info">
                <div class="file-name">${getFileIcon(file.name)} ${file.name}</div>
                <div class="file-size">${formatFileSize(file.size)}</div>
            </div>
            <button class="remove-file" onclick="removeFile(${index})">Remove</button>
        </div>
    `).join('');

    document.getElementById('fileCount').textContent = `${uploadedFiles.length} file${uploadedFiles.length !== 1 ? 's' : ''}`;
}

// Get File Icon
function getFileIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'pdf': '📄',
        'jpg': '🖼️',
        'jpeg': '🖼️',
        'png': '🖼️',
        'bmp': '🖼️',
        'tiff': '🖼️',
        'csv': '📊'
    };
    return icons[ext] || '📄';
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// Remove File
function removeFile(index) {
    uploadedFiles.splice(index, 1);
    updateFilesList();
}

// Clear All Files
function clearFiles() {
    if (uploadedFiles.length === 0) {
        showStatus('No files to clear!', 'error');
        return;
    }
    
    if (confirm('Are you sure you want to clear all files?')) {
        uploadedFiles = [];
        updateFilesList();
        clearResults();
        showStatus('All files cleared!', 'success');
    }
}

// Process Files
async function processFiles() {
    if (uploadedFiles.length === 0) {
        showStatus('Please select at least one file!', 'error');
        return;
    }

    const processBtn = document.getElementById('processBtn');
    const progressContainer = document.getElementById('progressContainer');

    // Disable button and show progress
    processBtn.disabled = true;
    progressContainer.style.display = 'block';

    try {
        const formData = new FormData();
        uploadedFiles.forEach(file => {
            formData.append('files[]', file);
        });

        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            extractedResults = data.results;
            currentSessionId = data.session_id;
            updateResults();
            showStatus(`Successfully processed ${data.results.length} file(s)!`, 'success');
            
            // Enable download tab
            document.getElementById('downloadEmpty').style.display = 'none';
            document.getElementById('downloadContent').style.display = 'block';
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        processBtn.disabled = false;
        progressContainer.style.display = 'none';
        updateProgress(0);
    }
}

// Update Results
function updateResults() {
    if (extractedResults.length === 0) {
        document.getElementById('resultsContainer').innerHTML = '<div class="empty-state"><p>No results available</p></div>';
        document.getElementById('resultsCount').textContent = '0 results';
        return;
    }

    document.getElementById('resultsCount').textContent = `${extractedResults.length} result${extractedResults.length !== 1 ? 's' : ''}`;

    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.innerHTML = extractedResults.map((result, index) => `
        <div class="result-item">
            <div class="result-filename">
                ${getFileIcon(result.filename)} ${result.filename}
                <span style="color: #95a5a6; font-size: 0.85rem; margin-left: 0.5rem;">(${result.pages} page${result.pages !== 1 ? 's' : ''})</span>
            </div>
            <div class="result-text">${escapeHtml(result.text.substring(0, 500))}</div>
            ${result.text.length > 500 ? '<div style="color: #667eea; font-size: 0.85rem; margin-top: 0.5rem;">... (view full text in page tab)</div>' : ''}
        </div>
    `).join('');

    // Populate page selector
    const pageSelect = document.getElementById('pageSelect');
    pageSelect.innerHTML = extractedResults.map((result, index) => 
        `<option value="${index}">${getFileIcon(result.filename)} ${result.filename}</option>`
    ).join('');

    // Show page nav
    document.getElementById('pageNav').style.display = 'flex';
}

// Update Progress
function updateProgress(percentage) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    progressFill.style.width = percentage + '%';
    progressText.textContent = percentage + '%';
}

// Switch Tab
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Deactivate all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Activate selected button
    event.target.classList.add('active');
}

// Page Navigation
function goToPage() {
    currentFileIndex = parseInt(document.getElementById('pageSelect').value);
    currentPageIndex = 0;
    displayPage();
}

function nextPage() {
    const result = extractedResults[currentFileIndex];
    if (currentPageIndex < result.pages - 1) {
        currentPageIndex++;
        displayPage();
    }
}

function previousPage() {
    if (currentPageIndex > 0) {
        currentPageIndex--;
        displayPage();
    }
}

function displayPage() {
    if (extractedResults.length === 0) return;

    const result = extractedResults[currentFileIndex];
    const pageContent = document.getElementById('pageContent');
    
    // Extract page content
    const pages = result.text.split('--- Page');
    let pageText = '';
    
    if (pages.length > 1) {
        pageText = pages[currentPageIndex + 1].replace(/^\s*\d+\s*---\n/, '');
    } else {
        pageText = result.text;
    }

    pageContent.innerHTML = `<div style="color: #2c3e50; line-height: 1.6;">${escapeHtml(pageText)}</div>`;

    // Update page buttons
    document.getElementById('prevPageBtn').disabled = currentPageIndex === 0;
    document.getElementById('nextPageBtn').disabled = currentPageIndex === result.pages - 1;

    // Update page info
    const pageInfo = `Page ${currentPageIndex + 1} of ${result.pages}`;
    const pageNav = document.getElementById('pageNav');
    let pageInfoSpan = pageNav.querySelector('.page-info');
    if (!pageInfoSpan) {
        pageInfoSpan = document.createElement('span');
        pageInfoSpan.className = 'page-info';
        pageNav.insertBefore(pageInfoSpan, pageNav.lastChild);
    }
    pageInfoSpan.textContent = pageInfo;
}

// Download Results
async function downloadResults(format) {
    if (!currentSessionId) {
        showStatus('No session found. Please process files first!', 'error');
        return;
    }

    try {
        const response = await fetch(`/download/${format}/${currentSessionId}`);
        
        if (!response.ok) {
            showStatus(`Error downloading ${format.toUpperCase()}!`, 'error');
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ocr_results_${new Date().toISOString().slice(0, 10)}.${format}`;
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);

        showStatus(`${format.toUpperCase()} downloaded successfully!`, 'success');
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Clear Results
function clearResults() {
    extractedResults = [];
    document.getElementById('resultsContainer').innerHTML = '<div class="empty-state"><p>No results available</p></div>';
    document.getElementById('resultsCount').textContent = '0 results';
    document.getElementById('pageContent').innerHTML = '<div class="empty-state"><p>Select a file to view pages</p></div>';
    document.getElementById('downloadEmpty').style.display = 'block';
    document.getElementById('downloadContent').style.display = 'none';
}

// Show Status Message
function showStatus(message, type = 'info') {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = 'block';

    setTimeout(() => {
        statusMessage.style.display = 'none';
    }, 4000);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Simulate progress
function simulateProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;
        updateProgress(Math.floor(progress));
        if (progress >= 90) clearInterval(interval);
    }, 300);
}