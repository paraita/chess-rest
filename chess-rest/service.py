from flask import Flask
from flask_restplus import Api, Resource, fields
from werkzeug.contrib.fixers import ProxyFix
from flask_restplus import reqparse

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Chessboard service',
          description='A simple Chessboard service')

ns = api.namespace('rest', description='Chessboard Rest interface')

move = api.model('Move', {
    'move': fields.String(required=True, description='The move in SAN format')
})


@ns.route('/spectator')
class WebView(Resource):
    '''Returns an html representation of the board'''
    @ns.doc('html representation of the board')
    def get(self):
        '''List all tasks'''
        return 'SPECTATOR VIEW HERE'


@ns.route('/')
class ChessRest(Resource):
    '''REST Interface of the Chessboard'''

    parser = ns.parser()
    parser.add_argument('move', required=True, help='move in SAN format', location='args')

    @ns.doc('Returns the board state')
    def get(self):
        '''Returns the board state in FEN format'''
        return 'BOARD STATE IN FEN FORMAT'

    @ns.expect(parser)
    def post(self):
        '''Make a move on the board'''
        args = self.parser.parse_args()
        print(args['move'])
        return f"{args}"


if __name__ == '__main__':
    app.run(debug=True)
