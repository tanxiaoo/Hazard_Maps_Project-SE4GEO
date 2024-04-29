from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def prova():
    return "<p>Facciamo progressi</p>"
