from flask import Flask, send_file, request, after_this_request, render_template
import requests
import os
from flask_restful import Resource, Api, reqparse
import cairosvg
app = Flask(__name__)
api = Api(app)


@app.route('/')
def read_me():
    return render_template('readme.html')

class SvgToPng(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('R', type=str, location='args')
        self.reqparse.add_argument('G', type=str, location='args')
        self.reqparse.add_argument('B', type=str, location='args')
        super().__init__()

    def get(self):
        argslist = self.reqparse.parse_args()

        r = requests.get('http://www.thecolorapi.com/id?rgb={},{},{}&w=150&h=150'.format(argslist['R'],argslist['G'],argslist['B']))
        response = r.json()
        image_url = response['image']['bare']
        cairosvg.svg2png(
            url= image_url, write_to='image.png')
        @after_this_request
        def remove_file(response):
            os.remove('./image.png')
            return response
        return send_file('image.png',mimetype='image/png')

api.add_resource(SvgToPng, '/image')

if __name__ == "__main__":
    app.run(port=6969, debug=True)
