#!/usr/bin/python

import os
import glob
import utter
import flask

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = flask.Flask("utter", template_folder=tmpl_dir, static_folder=static_dir)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/tts', methods=['POST', 'GET'])
def main():
    mp3s = []
    error = False
    if flask.request.method == 'POST':
        txt = flask.request.form['txt']
        lang = flask.request.form['lang']
        try:
            mp3dir = utter.tts(str(txt), source="en", target=lang)
            mp3s = glob.glob(os.path.join(mp3dir, "*.mp3"))
        except:
            error = True
    return flask.render_template('player.html', mp3s=mp3s, error=error)

@app.route('/<path:path>')
def catch_all(path):
    path = '/' + path
    folder, filename = os.path.split(path)
    return flask.send_from_directory(folder, filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
