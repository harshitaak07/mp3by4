document.getElementById('extractBtn').addEventListener('click', () => {
    const loadingElement = document.getElementById('result');
    loadingElement.innerText = "Processing your video, please wait...";

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.scripting.executeScript(
            {
                target: { tabId: tabs[0].id },
                function: extractText
            },
            async (result) => {
                const extractedText = result[0].result.join('\n\n');

                // Call backend server to summarize the text
                const summaryResponse = await fetch('http://localhost:5000/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: extractedText })
                });

                const summaryData = await summaryResponse.json();
                const summaryText = summaryData.summary;

                // Display the summary in the popup
                loadingElement.innerText = `Summary:\n${summaryText}\n\nProcessing video...`;

                // Call backend server to get the processed video URL
                const videoResponse = await fetch('http://localhost:5000/isolate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ videoPath: "path_to_your_video.mp4" })
                });

                const videoData = await videoResponse.json();
                const videoURL = `http://localhost:5000${videoData.videoURL}`;

                // Show video on the active tab in bottom-right corner
                chrome.scripting.executeScript({
                    target: { tabId: tabs[0].id },
                    func: displayVideoOnPage,
                    args: [videoURL]
                });

                // Update the popup message to indicate the video has been shown
                loadingElement.innerText += `\n\nVideo has been displayed on the webpage.`;
            }
        );
    });
});

// Function to extract text from the active webpage
function extractText() {
    const elements = document.body.querySelectorAll('h1, p, h2, h3, h4, h5, h6, div');
    let extractedText = [];
    elements.forEach((el) => {
        extractedText.push(el.innerText.trim());
    });

    const chunks = extractedText.join('\n\n').split(/\n\s*\n/); // Split into chunks
    return chunks;
}

// Function to display the video on the active webpage at the bottom-right corner
function displayVideoOnPage(videoURL) {
    const videoElement = document.createElement('video');
    videoElement.src = videoURL;
    videoElement.style.position = 'fixed';
    videoElement.style.bottom = '10px';
    videoElement.style.right = '10px';
    videoElement.style.width = '300px';
    videoElement.style.backgroundColor = 'transparent';
    videoElement.style.zIndex = '10000';
    videoElement.controls = true;

    document.body.appendChild(videoElement);

    // Make video element draggable
    let isDragging = false;
    let offsetX, offsetY;

    videoElement.addEventListener('mousedown', (e) => {
        isDragging = true;
        offsetX = e.clientX - videoElement.getBoundingClientRect().left;
        offsetY = e.clientY - videoElement.getBoundingClientRect().top;
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            videoElement.style.left = `${e.clientX - offsetX}px`;
            videoElement.style.top = `${e.clientY - offsetY}px`;
        }
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
    });
}

