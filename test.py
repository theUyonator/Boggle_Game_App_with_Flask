from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class BoggleTests(TestCase):
    """This test class holds integration tests for all the routes used in the boggle app"""
    def setUp(self):
        """Start up code to be run before testing"""
        app.config['TESTING'] = True

    def test_start_game(self):
        """This test method test the home route "/"""
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Get Ready To Boggle!!!!!</h1>", html)

    def test_display_board(self):
        """This test method test the information saved in session in the "/boggle/game" route"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["highscore"] = 20
                sess["nplays"] = 20

            resp = client.get("/boggle/game")

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session["highscore"], 20)
            self.assertEqual(session["nplays"], 20)

    def test_check_valid_word(self):
        """This function test the view function for the route /boggle/valid_word to confirm word is valid"""
        with app.test_client() as client:
            with client.session_transaction() as sess:
                sess["board"] = [   ["C", "A", "T", "Z", "A"],
                                    ["P", "C", "P", "O", "N"],
                                    ["O", "T", "A", "O", "T"],
                                    ["T", "E", "I", "W", "S"],
                                    ["S", "D", "N", "O", "D"]]

            resp = client.get("/boggle/valid_word?word=pain")

            self.assertEqual(resp.json["result"], "ok")


    def test_invalid_word(self):
        """This test function checks to see if the route /boggle/valid_word returns the expected output 
        for an invalid word or a word not on the board"""
        with app.test_client() as client:
            client.get("/boggle/game")
            response = client.get("/boggle/valid_word?word=norm") 
            self.assertEqual(response.json["result"], "not-on-board")

    def test_non_english_word(self):
        """This test function checks to see if the route /boggle/valid_word returns the expected output 
        for a non english word"""
        with app.test_client() as client:
            client.get("/boggle/game")
            response = client.get("/boggle/valid_word?word=mvht") 
            self.assertEqual(response.json["result"], "not-word")

    # def test_final_score(self):
    #     """This test function test to see if the view function for route "/boggle/final_score" makes the correct psot request"""
    #     with app.test_client() as client:
    #         client.post("/boggle/final_score", data={"score": 11})
    #         with client.session_trasaction() as sess:
    #             sess["highscore"] = 15

    #         response = client.get("/boggle/final_score")
    #         # import pdb
    #         # pdb.set_trace()

    #         self.assertEqual(response.json["brokeRecord"], True)

    def test_refresh(self):
        """This test function test to see if the view function refresh() redirects"""
        with app.test_client() as client:
            resp = client.get("/boggle/refresh")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/boggle/game")