from flask import Flask, request, jsonify
from model import main
from flask import jsonify

app = Flask(__name__)


@app.route('/my_user', methods=['GET'])
def my_user():
    """Perform the prediction using an API"""
    user_id = request.args.get('user_id')
    best_book, books_reco_culture = main(int(user_id))
    return jsonify({"Books_Read": best_book, "Books_Same_Culture": books_reco_culture})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
