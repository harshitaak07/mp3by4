document.getElementById('extractBtn').addEventListener('click', () => {
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

                // Display the summary in an alert
                alert(`Summary:\n${summaryText}`);

                // Call backend server to get the processed video URL
                const videoResponse = await fetch('http://localhost:5000/isolate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ videoPath: "path_to_your_video.mp4" })
                });

                const videoData = await videoResponse.json();
                const videoURL = videoData.videoURL;

                // Add a video element to the webpage with a transparent background
                chrome.scripting.executeScript({
                    target: { tabId: tabs[0].id },
                    func: displayVideoOnPage,
                    args: [videoURL]
                });
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

function displayVideoOnPage(videoURL) {
    print(videoURL)
    const videoElement = document.createElement('video');
    videoElement.src = videoURL;
    videoElement.style.position = 'fixed';
    videoElement.style.bottom = '10px';
    videoElement.style.right = '10px';
    videoElement.style.width = '300px';
    videoElement.style.background = 'transparent';
    videoElement.controls = true;
    document.body.appendChild(videoElement);
}
