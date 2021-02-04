from flask import Flask, redirect, request
from machine_Turing import MachineTuring
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel('INFO')

machine = MachineTuring()


@app.route('/', methods=['GET'])
def get():
    return machine.render()


@app.route('/update', methods=['POST'])
def update():
    try:
        machine.update_all()
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


@app.route('/start', methods=['POST'])
def start():
    try:
        machine.update_all()
        machine.start(int(request.form.get('steps')))
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


@app.route('/next_step', methods=['POST'])
def next_step():
    try:
        machine.update_all()
        machine.start(1)
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


@app.route('/save', methods=['POST'])
def save():
    try:
        machine.update_all()
        machine.save(request.form.get('save-load'))
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


@app.route('/load', methods=['POST'])
def load():
    try:
        machine.load(request.form.get('save-load'))
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


@app.route('/clear', methods=['POST'])
def clear():
    try:
        machine.clear()
    except Exception as e:
        logger.warning(e)
        return redirect('/')
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
