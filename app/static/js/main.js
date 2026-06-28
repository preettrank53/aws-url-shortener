/**
 * Copies the shortened URL input text from the main result card.
 */
function copyToClipboard() {
    const copyInput = document.getElementById("shortenedUrl");
    const copyButton = document.getElementById("copyBtn");
    
    if (!copyInput) return;
    
    // Select the text field
    copyInput.select();
    copyInput.setSelectionRange(0, 99999); // For mobile devices
    
    // Copy the text inside the text field
    navigator.clipboard.writeText(copyInput.value)
        .then(() => {
            // Visual feedback
            const originalHTML = copyButton.innerHTML;
            copyButton.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
            copyButton.classList.add("copied");
            
            // Revert back after 2 seconds
            setTimeout(() => {
                copyButton.innerHTML = originalHTML;
                copyButton.classList.remove("copied");
            }, 2000);
        })
        .catch(err => {
            console.error("Could not copy link to clipboard: ", err);
        });
}

/**
 * Copies a specific short URL text from a table button actions list.
 * @param {string} text - The text to copy.
 * @param {HTMLElement} btn - The button element that triggered the copy.
 */
function copyText(text, btn) {
    if (!text || !btn) return;
    
    navigator.clipboard.writeText(text)
        .then(() => {
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-check" style="color: #10b981;"></i>';
            
            setTimeout(() => {
                btn.innerHTML = originalHTML;
            }, 2000);
        })
        .catch(err => {
            console.error("Could not copy: ", err);
        });
}

// Client-side URL format validation fallback
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("shortenForm");
    const originalUrlInput = document.getElementById("originalUrl");
    
    if (form && originalUrlInput) {
        form.addEventListener("submit", (e) => {
            const urlVal = originalUrlInput.value.trim();
            if (!urlVal.startsWith("http://") && !urlVal.startsWith("https://")) {
                e.preventDefault();
                alert("Please enter a valid URL starting with http:// or https://");
            }
        });
    }
});
