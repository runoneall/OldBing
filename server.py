import os
import flask
import crawler

app = flask.Flask(__name__)

@app.route('/')
def main():
    return flask.render_template('main.html')

@app.route('/search', methods=['GET','POST'])
def search():
    if flask.request.method == 'GET':
        args = flask.request.args
        if 'q' in args:
            query_str = args.get('q')
            query = query_str.replace(' ', '+')
            RepDict = crawler.Crawler(f'/search?q={query}')
            return flask.render_template(
                'search.html', 
                results = RepDict['results'], 
                target_search = query_str
            )
        return flask.redirect('/')
    if flask.request.method == 'POST':
        search_input = flask.request.form['search_input']
        search_input = search_input.replace(' ', '+')
        return flask.redirect(f'/search?q={search_input}')
    
@app.route('/search-api', methods=['GET'])
def search_api():
    if flask.request.method == 'GET':
        args = flask.request.args
        if 'q' in args:
            query_str = args.get('q')
            query = query_str.replace(' ', '+')
            query = query_str.replace('%20', '+')
            RepDict = crawler.Crawler(f'/search?q={query}')
            return flask.jsonify(RepDict)
        return flask.render_template('api_doc.html')

@app.route('/logo')
def logo():
    logo_path = './logo.png'
    if os.path.exists(logo_path):
        return flask.send_file(logo_path, mimetype='image/jpeg')
    
@app.route('/favicon.ico')
def favicon():
    favicon_path = './favicon.ico'
    if os.path.exists(favicon_path):
        return flask.send_file(favicon_path, mimetype='image/x-icon')
    
app.run(
    host='0.0.0.0',
    port=8501,
    debug=True,
    threaded=True
)
