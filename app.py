from flask import Flask, config, render_template, request
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return gm(request.args.get('data'))