from flask import Flask, request, jsonify
import sys
import traceback
from io import StringIO

app = Flask(__name__)


@app.route('/py', methods=['POST'])
def py():
    code = request.form['code']
    output = ''
    error = None
    local_vars = {}

    try:
        # Salida estándar a un buffer
        stdout_capture = StringIO()
        sys.stdout = stdout_capture

        exec(code, None, local_vars)
        output = stdout_capture.getvalue()

    except Exception:
        error = traceback.format_exc()
    
    finally:
        # Restaurar la salida estándar original
        sys.stdout = sys.__stdout__
    
    response = {
        "code": code,
        "output":output,
        "error":error
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
