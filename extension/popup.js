document.getElementById('extractBtn').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript(
            {
                target: { tabId: tabs[0].id },
                function: extractText
            },
            (result) => {
                const extractedText = result[0].result.join('\n\n'); // Joining chunks into a single string
                const blob = new Blob([extractedText], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);

                // Create a link element to download the text file
                const a = document.createElement('a');
                a.href = url;
                a.download = 'extracted_text.txt'; // Filename
                document.body.appendChild(a);
                a.click(); // Simulate click to download
                document.body.removeChild(a); // Remove the link element
                URL.revokeObjectURL(url); // Free memory
            }
        );
    });
});

function extractText() {
    const elements = document.body.querySelectorAll('h1, p, h2, h3, h4, h5, h6, div');
    let extractedText = [];
    elements.forEach((el) => {
        extractedText.push(el.innerText.trim());
    });

    // Split the extracted text into chunks based on double new lines
    const chunks = extractedText.join('\n\n').split(/\n\s*\n/); // Splitting based on one or more new lines
    return chunks;
}
