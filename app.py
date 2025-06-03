from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask API is running!"

@app.route('/extract', methods=['GET'])
def extract_from_url():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Thiếu tham số url'}), 400
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'Không có tiêu đề'
        paragraphs = soup.find_all('p')
        content = '\n'.join(p.get_text() for p in paragraphs[:10])
        return jsonify({'url': url, 'title': title.strip(), 'content': content.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
