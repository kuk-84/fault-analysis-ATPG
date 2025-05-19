from flask import Flask, render_template
import os

try:
    import generatenetlist
except Exception as e:
    generatenetlist = None
    error_on_import = e

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/SomeFunction")
def SomeFunction():
    try:
        if generatenetlist is None:
            raise ImportError(error_on_import)
        
        result = generatenetlist.generate_netlist()
        return render_template("result.html", result=result)
    
    except Exception as e:
        return f"<pre>⚠️ Internal Server Error:\n{str(e)}</pre>", 500
