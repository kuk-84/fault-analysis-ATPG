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

@app.route("/SomeFunction")
def SomeFunction():
    try:
        import generatenetlist
        result = generatenetlist.generate_netlist()
        return render_template("result.html", result=result)
    except Exception as e:
        return f"<pre>⚠️ Internal Server Error:\n{str(e)}</pre>", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
