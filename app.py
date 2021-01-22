from flask import Flask, request, render_template, redirect, session, jsonify, flash
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config["SECRET_KEY"] = "uh9v3t0und3rst9nd"

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def start_game():
    """This function renders the start page for the boogle game"""
    highscore = session.get("highscore", 0)
    return render_template("index.html", highscore=highscore)

@app.route("/boggle/game")
def display_board():
    """This function will display the game board and intiate session storage for the highscore and number of times played"""
    board = boggle_game.make_board()
    session["board"] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("boggle_game.html", board=board, highscore=highscore, nplays=nplays)

@app.route("/boggle/valid_word")
def check_valid_word():
    """This function checks a word sent to this route to see if it is in the Boggle Game word dictionary
        it returns JSON confirming if the word exist or not
        """
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({"result": res})
@app.route("/boggle/final_score", methods=["POST"])
def final_score():
    """This function receives the current score, updates the number of plays and if necessary updates high score"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session["nplays"] = nplays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(brokeRecord = score > highscore)

@app.route("/boggle/refresh")
def refresh():
    """This function redirects the user to start the game again"""
    return redirect("/boggle/game")