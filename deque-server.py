from flask import Flask
app = Flask(__name__)

@app.route('/search/<showname>')
def search(showname):
    return '{%s}' % (showname)

@app.route('/add/<magnet>/')
def add(magnet):
    return magnet

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    

