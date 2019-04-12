import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from flask_prometheus import setup_metrics
from prometheus_client import generate_latest
import fib

""" 
Sample web service to provide Fibonacci sequence. Using Flask for
demonstration purposes. 
"""

class RequestFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        record.path = request.path
        record.full_path = request.full_path
        record.method = request.method
        return super().format(record)


app = Flask(__name__)
setup_metrics(app)

@app.route('/')
def hello():
    return "Please visit /fibseq/NUMBER url to get Fibonacci sequence or /fib/NUMBER to get Fibonacci number.\n"

@app.route('/fibseq/<num>')
def show_fibonacci_sequence(num):
    if num[0] == '-':
        app.logger.warning("Negative value received: %s" % num)
        return jsonify({'input': num,
            'error': 'Negative value, service accepts only non-negative numbers', 'sequence': None}
            ), 400

    try:
        sequence = fib.fib_sequence(int(num))
        return jsonify({'input': num, 'error': None, 'sequence': sequence}), 200
    except ValueError as e:
        app.logger.warning("Invalid input: %s" % str(e))
        return jsonify({'input': num, 'error': str(e), 'sequence': None}), 400
    except Exception as e:
        app.logger.error("Error while processing request: %s" % str(e))
        raise

@app.route('/cache')
def show_cache():
    return jsonify(fib.cache())

@app.route('/metrics')
def metrics():
    return generate_latest()


if __name__ == "__main__":
    # setup logging
    app.logger = logging.getLogger(__name__)
    handler = RotatingFileHandler('/logs/flask.log', mode='a', maxBytes=1000000, backupCount=5)
    formatter = RequestFormatter('%(asctime)s: %(name)s - %(levelname)s - %(remote_addr)s "%(method)s %(path)s" "%(message)s"')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.run(host="0.0.0.0", debug=False)
