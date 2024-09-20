// Get the active tab's URL and display it in the popup
chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    var currentTab = tabs[0]; // Current active tab
    var currentUrl = currentTab.url; // Get URL of the current tab
    document.getElementById('url').textContent = currentUrl; // Display the URL
});
