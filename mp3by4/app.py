from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from prisma import Prisma

app = Flask(__name__)
db = Prisma()

@app.before_first_request
async def init_db():
    await db.connect()

@app.route('/webpages', methods=['GET'])
async def get_webpages():
    webpages = await db.web_page.find_many()
    return {'webpages': webpages}

@app.teardown_appcontext
async def close_db(exception):
    await db.disconnect()

if __name__ == '__main__':
    app.run()
