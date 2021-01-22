/*
This JS file will  use AJAX concepts and DOM manipulation to craete a new Boggle game 
and provide the full functionality of the Boggle game.

*/

class BoggleGame{

    constructor(boardId, secs=60){
        // The boggle game is to take 60secs
        this.secs = secs;
        // Select the section holding the board in the html and set it to a variable
        this.board=$("#" + boardId);
        // Because we do not want repetitions of words, a variable is created and is made a Set
        this.words = new Set();
        // Set the initial score to equal zero, when a valid word is found, the length of the word will be added to the score
        this.score = 0;
        // Set the timer to reduce every 1000msec
        this.timer = setInterval(this.tick.bind(this), 1000);
        // Show the timer on the DOM
        this.showTimer();
        // $(".add-word", this.board).on("submit","button",this.handleSubmit(evt))

        $("#guess_btn").on("click", this.handleSubmit.bind(this));

    }

    showMessage(msg, cls){
        // This function will select the paragraph tag on the html and display the message on the word coming from the server
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }

    showWord(word){
        // This function will create an li and display valid words on the DOM
        let $li = $(`<li>${word}</li>`);
        const word_list = $(".words", this.board);
        word_list.append($li);
    }
    showScore(){
        // This function displays the score in the DOM
        $(".score", this.board).text(this.score);

    }

    showTimer(){
        // This function displays the timer on the DOM
        $(".timer", this.board).text(this.secs)
    }

    async handleSubmit(evt){
        // Use preventDefault from prevent the default behaviour of the page to refresh when a form is submitted
        evt.preventDefault();
        // Select the input where the guess is entered and set it to a variable, const is better here because the input will not be changing 
        const $word = $(".word", this.board);
        // The value of the input however will so we set it to a variable using let
        let word = $word.val()
        // If the input box is empty when the form is submitted, do nothing
        if(!word) return
        // Check that the set where previously created words are stored has the new word guessed
        if(this.words.has(word)){
            this.showMessage(`Already have ${word}`, "error");
            return;
        }

        // Then the server is checked to see if the word exist, we use AJAX to send a get request

        const response = await axios.get("/boggle/valid_word", {params:{word:word}})
        if(response.data.result === "not-word"){
            this.showMessage(`${word} is not a valid english word`, "error");
        }
        else if(response.data.result === "not-on-board"){
            this.showMessage(`${word} is not a valid word on the board`, "error");
        }
        else{
            this.showMessage(`Word ${word} has been added`, "ok");
            this.showWord(word);
            this.score += word.length;
            this.words.add(word)
            this.showScore()
        }

        $word.val("").focus();


    }

    async tick(){
        // This methods reduces the time
        this.secs -= 1; 
        this.showTimer();
        if(this.secs === 0){
            clearInterval(this.timer);
            await this.scoreGame();
        }
    }

    async scoreGame(){
        $(".add-word", this.board).hide();
        const res = await axios.post("/boggle/final_score", {score: this.score});
        if(res.data.brokeRecord){
            this.showMessage(`New record: ${this.score}`, "ok")
        }
        else{
            this.showMessage(`Final score: ${this.score}`, "ok")
        }
        $("#refresh", this.board).show();
    }

}

let game = new BoggleGame("boggle_game", 60);

