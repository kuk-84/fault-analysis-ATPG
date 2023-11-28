import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')
import generatenetlist
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/SomeFunction')
def SomeFunction():
    print('In SomeFunction')
    result = generatenetlist.generate_netlist()
    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
