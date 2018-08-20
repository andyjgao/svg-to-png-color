# -------------------------------------------------------------------------------
# Author: Chase Midler, Andy Gao
# -------------------------------------------------------------------------------
# Tools uses:
# Flask,Python
# -------------------------------------------------------------------------------
from flask import Flask, send_file, request, after_this_request, render_template
import requests
import os
from flask_restful import Resource, Api, reqparse
import cairosvg
app = Flask(__name__)
api = Api(app)


# @route GET /
# @desc Read me page on how to use API
# @access Public
@app.route('/')
def read_me():
    return render_template('readme.html')


# @route GET /image?
# @desc Given an RGB, displays a 200 x 200 px of the color in png for temp use, then deletes image after request
# @access Public
class SvgToPng(Resource):
    def __init__(self):

        # Initialized arguments that can be added
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('R', type=str, location='args')
        self.reqparse.add_argument('G', type=str, location='args')
        self.reqparse.add_argument('B', type=str, location='args')
        super().__init__()

    def get(self):
        
        # adds arguments from url to list 
        argslist = self.reqparse.parse_args()

        # sends request for svg color of the image 
        r = requests.get('http://www.thecolorapi.com/id?rgb={},{},{}&w=150&h=150'.format(argslist['R'],argslist['G'],argslist['B']))
        response = r.json()
        image_url = response['image']['bare']
        
        # converts svg image into png 
        cairosvg.svg2png(
            url= image_url, write_to='image.png', scale= 2)
        
        # deletes image after request
        @after_this_request
        def remove_file(response):
            os.remove('./image.png')
            return response
        return send_file('image.png',mimetype='image/png')

api.add_resource(SvgToPng, '/image')

if __name__ == "__main__":
    app.run(port=6969, debug=True)