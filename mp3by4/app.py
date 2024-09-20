from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from prisma import Prisma
from text_extract import extract_text_from_url  # Import your extraction function

app = Flask(__name__)
db = Prisma()

@app.before_first_request
async def init_db():
    await db.connect()

@app.route('/extract/<int:webpage_id>', methods=['GET'])
async def extract(webpage_id):
    # Fetch the webpage data from the database using the provided ID
    webpage = await db.web_page.find_unique(where={'id': webpage_id})
    
    if not webpage:
        return jsonify({'error': 'Webpage not found'}), 404

    url = webpage.url  # Get the URL from the database

    # Extract text from the URL
    text = extract_text_from_url(url)
    title = "Your logic to extract the title"  # Implement title extraction logic if needed

    # Update the webpage entry in the database with the extracted text
    updated_webpage = await db.web_page.update(
        where={'id': webpage_id},
        data={'text': text, 'title': title}
    )

    return jsonify(updated_webpage), 200

@app.route('/webpages', methods=['GET'])
async def get_webpages():
    webpages = await db.web_page.find_many()
    return {'webpages': webpages}

@app.teardown_appcontext
async def close_db(exception):
    await db.disconnect()

if __name__ == '__main__':
    app.run(debug=True)
