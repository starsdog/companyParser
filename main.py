from flask import Flask,Blueprint
import init

import api.api_graph as api_graph
import api.api_group as api_group

app = Flask(__name__)
prefix_url='/company'
app.register_blueprint(api_graph.mod, url_prefix=prefix_url+'/graph')
app.register_blueprint(api_group.mod, url_prefix=prefix_url+'/group')

@app.route(prefix_url+'/')
def hello_world():
    return 'Welcome to relation web!'

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0')

