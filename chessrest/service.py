from flask_restplus import Api, Resource, fields
from flask import render_template
from flask import Response
import chess
import chess.svg

api = Api(version='1.0', title='Chessboard service',
          description='A simple Chessboard service')
ns = api.namespace('rest', description='Chessboard Rest interface')
viz = api.namespace('viz', description='Chessboard Representation')
board = chess.Board()

move = api.model('Move', {
    'move': fields.String(required=True, description='A move in UCI format')
})

@ns.route('')
class ChessRest(Resource):
    '''REST Interface of the Chessboard'''

    parser = ns.parser()
    parser.add_argument('move', required=True, help='move in SAN format', location='args')

    @ns.doc('Returns the board state')
    def get(self):
        '''Returns the board state in FEN format'''
        response = Response(board.fen(), mimetype='text/plain')
        return response

    @ns.expect(move)
    def post(self):
        '''Make a move on the board'''
        payload = api.payload
        try:
            uci_move = payload['move']
            board.push_uci(uci_move)
            return Response('Move registered !', 200)
        except ValueError as err:
            print(err)
            return Response('Invalid move: {}'.format(move), 405)


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
