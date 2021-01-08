from flask import Flask, render_template, make_response, request, redirect, url_for
import psycopg2
import psycopg2.extras
import dicttoxml
import os
from dotenv import load_dotenv
from zimoti_scraping import export_csv
import glob
import csv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def zimoti_scraping():
    if request.method == 'POST':
        days = request.form['days']
        if days.isdigit():
            return redirect(url_for('zimoti_result', days=days))
    return render_template('zimoti_scraping.html')

@app.route('/scraping/<string:days>')
def zimoti_result(days):
    export_csv(str(days))
    files = glob.glob('C:/Users/kzyik/D_Files/PYTHON_FILES/DB/herokuPostgresql/csv/*.csv')
    latest_file = max(files, key=os.path.getctime)
    fieldnames = ['title', 'url', 'user_name']
    items_list = []
    with open (latest_file, 'r') as f:
        conn = psycopg2.connect(dbname=os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"), port=os.environ.get("DB_PORT"))
        with conn:
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT title FROM test_schema.test_table;")
                titles = [i[0] for i in cur.fetchall()]
                for row in csv.DictReader(f, fieldnames=fieldnames):
                    if row['title'] in titles:
                        pass
                    else:
                        cur.execute(f"INSERT INTO test_schema.test_table (title, url, user_name) VALUES (%s, %s, %s);", (row['title'], row['url'], row['user_name'] ))
                        item_dict = {}
                        item_dict['title'] = row['title']
                        item_dict['url'] = row['url']
                        item_dict['user_name'] = row['user_name']
                        items_list.append(item_dict)
    return render_template('zimoti_result.html', items_list=items_list)


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