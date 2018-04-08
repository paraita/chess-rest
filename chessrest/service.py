from flask_restplus import Api, Resource
from flask import render_template
from flask import Response
import chess
import chess.svg

api = Api(version='1.0', title='Chessboard service',
          description='A simple Chessboard service')
ns = api.namespace('rest', description='Chessboard Rest interface')
viz = api.namespace('viz', description='Chessboard Representation')
board = chess.Board()


@ns.route('/')
class ChessRest(Resource):
    '''REST Interface of the Chessboard'''

    parser = ns.parser()
    parser.add_argument('move', required=True, help='move in SAN format', location='args')

    @ns.doc('Returns the board state')
    def get(self):
        '''Returns the board state in FEN format'''
        return board.fen()

    @ns.expect(parser)
    def post(self):
        '''Make a move on the board'''
        args = self.parser.parse_args()
        if 'move' in args:
            board.push_san(args['move'])
            return Response('Move registered !', 200)
        else:
            return Response('UH OH You forgot the move parameter', 405)


@ns.route('/reset')
class ResetBoardState(Resource):
    '''Reset the chest board the chess board'''

    @ns.doc('Reset the chest board the chess board')
    def post(self):
        '''Reset the chest board the chess board'''
        board.reset()
        return 'Board reset !', 200


@viz.route('/board')
class ImageRepresentation(Resource):
    '''Image representation of the chess board'''

    @ns.doc('Returns the board svg representation')
    def get(self):
        '''Returns the board svg representation'''
        image = chess.svg.board(board=board)
        response = Response(image, mimetype='image/svg+xml')
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.cache_control.max_age = 0
        return response


@viz.route('/spectator')
class WebView(Resource):
    '''Returns an html representation of the board'''
    @ns.doc('html representation of the board')
    def get(self):
        '''Returns and HTML representation of the board'''
        response = render_template('hello.html')
        return Response(response, mimetype='text/html')
