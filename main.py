from flask import Flask,Blueprint
import api_graph

app = Flask(__name__)
prefix_url='/relation'
app.register_blueprint(api_graph.mod, url_prefix=prefix_url+'/graph')


@app.route(prefix_url+'/')
def hello_world():
    return 'Welcome to relation web!'

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')

