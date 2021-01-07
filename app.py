from flask import Flask, render_template, make_response
import psycopg2
import psycopg2.extras
import dicttoxml
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)


app = Flask(__name__)

@app.route('/')
def home():
    message = 'heroku postgresql test'
    return render_template('index.html', message=message)

@app.route('/xml')
def return_xml():
    conn = psycopg2.connect(dbname=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"), port=os.environ.get("DB_PORT"))
    with conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('SELECT to_json(test_table) FROM test_schema.test_table')
            result = cur.fetchall()
            table_data = []
            for d in result:
                table_data.append(d[0])
    xml = dicttoxml.dicttoxml(table_data)
    response = make_response(xml)
    response.headers['Content-Type'] = 'text/xml'
    return response

if __name__ == '__main__':
    app.run(debug=True)