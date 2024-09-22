document.getElementById("extractBtn").addEventListener("click", () => {
    const loadingElement = document.getElementById("result");
    loadingElement.innerText = "Processing your video and text, please wait...";
  
    // Get the current active tab URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTabUrl = tabs[0].url;
  
      chrome.scripting.executeScript(
        {
          target: { tabId: tabs[0].id },
          function: extractText, // Not needed, but kept for other parts
        },
        async (result) => {
          // Call backend server to generate narration based on webpage URL
          const narrationResponse = await fetch(
            "http://localhost:5000/generate_narration",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ url: activeTabUrl }), // Pass the active tab URL
            }
          );
  
          if (narrationResponse.ok) {
            const narrationData = await narrationResponse.json();
            const narrativeText = narrationData.narrative;
            const mp3URL = `http://localhost:5000${narrationData.mp3_url}`;
  
            console.log("Narrative Text:", narrativeText); // Log the narrative text
            console.log("MP3 URL:", mp3URL); // Log the MP3 URL
  
            // Display the generated narration in the popup
            loadingElement.innerText += `\n\nNarrative:\n${narrativeText}\n\nNarration audio is ready`;
  
            // Display the MP3 audio player for the narration
            const audioElement = document.createElement("audio");
            audioElement.controls = true;
            audioElement.src = mp3URL;
            loadingElement.appendChild(audioElement);
          } else {
            loadingElement.innerText += "\nFailed to generate narration.";
            console.error(
              "Failed to generate narration:",
              await narrationResponse.json()
            );
          }
  
          // Continue processing the video (assuming this part is still needed)
          const videoResponse = await fetch("http://localhost:5000/process_and_combine", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ videoPath: "static/amongus.mp4",url:activeTabUrl }), // Specify the video path
          });
  
          const videoData = await videoResponse.json();

          const videoURL = `http://localhost:5000${videoData.videoURL}`;
          console.log("Video URL:", videoURL); // Log the video URL
  
          // Show video on the active tab in bottom-right corner
          chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: displayVideoOnPage,
            args: [videoURL],
          });
  
          loadingElement.innerText += `\n\nVideo has been displayed on the webpage`;
        }
      );
    });
  });
  
  // Function to extract text from the active webpage
  function extractText() {
    const elements = document.body.querySelectorAll(
      "h1, p, h2, h3, h4, h5, h6, div"
    );
    let extractedText = [];
    elements.forEach((el) => {
      extractedText.push(el.innerText.trim());
    });
  
    const chunks = extractedText.join("\n\n").split(/\n\s*\n/); // Split into chunks
    return chunks;
  }
  
  // Function to display the video on the active webpage at the bottom-right corner
  function displayVideoOnPage(videoURL) {
    const videoElement = document.createElement("video");
    videoElement.src = videoURL;
    videoElement.style.position = "fixed";
    videoElement.style.bottom = "10px";
    videoElement.style.right = "10px";
    videoElement.style.width = "300px";
    videoElement.style.backgroundColor = "transparent";
    videoElement.style.zIndex = "10000";
    videoElement.controls = true;
  
    document.body.appendChild(videoElement);
  
    // Make video element draggable
    let isDragging = false;
    let offsetX, offsetY;
  
    videoElement.addEventListener("mousedown", (e) => {
      isDragging = true;
      offsetX = e.clientX - videoElement.getBoundingClientRect().left;
      offsetY = e.clientY - videoElement.getBoundingClientRect().top;
    });
  
    document.addEventListener("mousemove", (e) => {
      if (isDragging) {
        videoElement.style.left = `${e.clientX - offsetX}px`;
        videoElement.style.top = `${e.clientY - offsetY}px`;
      }
    });
  
    document.addEventListener("mouseup", () => {
      isDragging = false;
    });
  }