chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const url = tabs[0].url; // Get current tab URL
  const classification = "concept_learning"; // Define your classification

  fetch("http://your-backend-url/extract", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url, classification }),
  })
    .then((response) => response.json())
    .then((data) => console.log("Data saved:", data))
    .catch((error) => console.error("Error:", error));
});
