document.getElementById('extractBtn').addEventListener('click', () => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.scripting.executeScript(
        {
          target: { tabId: tabs[0].id },
          function: extractText
        },
        (result) => {
          document.getElementById('result').textContent = result[0].result;
        }
      );
    });
  });
  
  function extractText() {
    const elements = document.body.querySelectorAll('h1, p, h2, h3, h4, h5, h6, div');
    let extractedText = '';
    elements.forEach((el) => {
      extractedText += el.innerText + '\n\n';
    });
    return extractedText;
  }
  