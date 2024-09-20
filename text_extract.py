import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Failed. Status code: {response.status_code}"
    
    soup = BeautifulSoup(response.content, 'html5lib')
    
    for script_or_style in soup(['script', 'style', 'noscript', 'header', 'footer', 'aside', 'nav']):#removing styles/css
        script_or_style.decompose()

    text_elements = []
    for tag in soup.find_all(['h1', 'p', 'h2', 'h3', 'h4', 'div', 'h5', 'h6']):
        text = tag.get_text(strip=True)
        if text:
            text_elements.append(text + '\n') 

    full_text = '\n\n'.join(text_elements)
    
    return full_text

# Example usage
url = 'https://aws.amazon.com/what-is/quantum-computing/#:~:text=Quantum%20computing%20is%20a%20multidisciplinary,faster%20than%20on%20classical%20computers.'  # Replace with the URL of your choice
extracted_text = extract_text_from_url(url)
print(extracted_text)
