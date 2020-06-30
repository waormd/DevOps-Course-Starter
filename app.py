from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/', methods=['POST'])
def indexPost():
    item = request.form['item']
    session.add_item(item)
    return index(session.get_items())

@app.route('/', methods=['GET'])
def indexGet():
    return index(session.get_items())

def index(sessionItems):
    return render_template('index.html', items = sessionItems)


if __name__ == '__main__':
    app.run()
