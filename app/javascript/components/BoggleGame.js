import React from "react"
import { connect} from 'react-redux'
import {createStructuredSelector} from "reselect";
import Styles from "./Styles"

const START_GAME_REQUEST = 'START_GAME_REQUEST';
const START_GAME_SUCCESS = 'START_GAME_SUCCESS';

const SUBMIT_WORD_REQUEST = 'SUBMIT_WORD_REQUEST';
const SUBMIT_WORD_SUCCESS = 'SUBMIT_WORD_SUCCESS';
const SUBMIT_WORD_FAILED = 'SUBMIT_WORD_FAILED';

const CLEAR_WORD_REQUEST = 'CLEAR_WORD_REQUEST';
const CLEAR_WORD_SUCCESS = 'CLEAR_WORD_SUCCESS';

const ADD_LETTER_REQUEST = 'ADD_LETTER_REQUEST';
const ADD_LETTER_SUCCESS = 'ADD_LETTER_SUCCESS';

//This function all server api to load the game board data, which is 4x4 array of random letters
function startGame(){
  console.log('starGame() Action!!')
  return dispatch => {
      dispatch({type:START_GAME_REQUEST});
      return fetch(`v1/boggle_game.json`)
          .then(response => response.json())
          .then(json => dispatch(startGameSuccess(json)))
          .catch(error => console.log((error)))
  }
}

//This method calling wordapi to validate word from client side.  Currently NOT being use.
function submitWord_client(word, allWords){
    console.log('submitWord() Action!!');
    console.log('submitted word is: ' + word.join(""));
    if(word.length == 0){
        alert("There is no word to submit.  Action aborted");
        return;
    }
    if(word.length < 3){
        alert("The word is too short. The length of 3 or longer is required.  Action aborted");
        return;
    }
    if(allWords.includes(word)){
        alert("The word has previously been submitted.  Action aborted");
        return;
    }

    let url = "https://wordsapiv1.p.rapidapi.com/words/" + word.join("") + "/definition"
    return dispatch => {
        dispatch({type: SUBMIT_WORD_REQUEST});
        return fetch(url,
            {
                    method: "GET",
                    headers: {
                        "x-rapidapi-host": "wordsapiv1.p.rapidapi.com",
                        "x-rapidapi-key": "9ca4422241mshe0286c9a9674497p14d0e5jsn7d6a927fd826"
                    }
                })
            .then(function (response) {
                let status = response.status;
                if(status == 200){
                    dispatch(submitWordSuccess(response.json()));
                }
                else{
                    dispatch(submitWordFailed(response.json()));
                }
            })
            .catch(error => console.log((error)))
    }
}

//This method calls server which in turn calls word api to validate word.  Currently being used
function submitWord(word, allWords){
    console.log('submitWord() Action!!');
    if(word.length == 0){
        return dispatch => {
            dispatch({type: SUBMIT_WORD_REQUEST});
            return dispatch(submitWordFailed({message: "There is no word to submit.  Action aborted"}));
        }
    }
    if(word.length < 3){
        return dispatch => {
            dispatch({type: SUBMIT_WORD_REQUEST});
            return dispatch(submitWordFailed({message: "Word must contain three or more character.  Action aborted"}));
        }
    }
    if(allWords.includes(word.join(""))){
        return dispatch => {
            dispatch({type: SUBMIT_WORD_REQUEST});
            return dispatch(submitWordFailed({message: "The word has previously been submitted.  Action aborted"}));
        }
    }

    let url = "v1/boggle_game/" + word.join("") + ".json"
    return dispatch => {
        dispatch({type: SUBMIT_WORD_REQUEST});
        return fetch(url)
            .then(response  => response.json())
            .then(function(response) {
                if (response.valid == true) {
                    dispatch(submitWordSuccess())
                } else {
                    dispatch(submitWordFailed({message: "Invalid word: " + word.join("")}))
                }
            })
            .catch(error => console.log((error)))
    }
}
//clear the word in order to build a new one
function clearWord(){
    console.log('clearWord() Action!!');
    return dispatch => {
        dispatch({type: CLEAR_WORD_REQUEST});
        return dispatch(clearWordSuccess());
    }
}

//Add letter from selected cell to build the word
function addLetter(i, j, letter, selectedCells) {
    console.log('addLetter() Action!!');
    return dispatch => {
        dispatch({type: ADD_LETTER_REQUEST});
        return dispatch(addLetterSuccess({letter: letter, i: i, j: j}));
    }
}

export function startGameSuccess(json) {
    return {
        type: START_GAME_SUCCESS,
        json
    }
}

export function clearWordSuccess() {
    return {
        type: CLEAR_WORD_SUCCESS
    }
}

    export function addLetterSuccess(json) {
    return {
        type: ADD_LETTER_SUCCESS,
        json
    }
}

export function submitWordSuccess() {
    return {
        type: SUBMIT_WORD_SUCCESS
    }
}

export function submitWordFailed(json) {
    console.log(json);
    return {
        type: SUBMIT_WORD_FAILED,
        json
    }
}


class BoggleGame extends React.Component {
    render () {
      const {gameBoard} = this.props;
      const {selectedCells} = this.props;
      const {currentWord} = this.props;
      const {totalScore} = this.props;
      const {allWords} = this.props;

      const resultStyle = allWords.length == 0 ? {display: 'none'}: {};
      const actionStyle = currentWord.length > 0 ? {}: {display: 'none'}
      const tipStyle = this.props.start && currentWord.length == 0 ? {}: {display: 'none'}
      const rows = gameBoard.map((items, i) =>
          <tr key={i}>{items.map((item, j) =>
            <td key={j} align="center">
                <button onClick={() => this.props.addLetter(i, j, item.letter, selectedCells)} style={!item.selected? Styles.availableButton : Styles.selectedButton} disabled={item.selected}><h1>{item.letter}</h1></button>
            </td>)}
          </tr>);
      const wordList = allWords.map((word) => {return <li style={Styles.noBullet}>{word}</li>});
      return (
      <React.Fragment>
          <div align="center">
              <h1>Boggle Game</h1>
              <button className="getThingBtn" onClick={() => this.props.startGame()} style={Styles.startButton}>Start Game</button>
              <br/>
              <br/>
              <table className="table" border="1" >
                <tbody>{rows}</tbody>
              </table>
              <br/>
              <div style={actionStyle}>
                  Your word is: {currentWord.join("")}
                <br />
                <br />
                <button onClick={() => this.props.submitWord(currentWord, allWords)} style={Styles.submitButton}>Submit Word</button><button onClick={() => this.props.clearWord()} style={Styles.clearButton}>Clear Word</button>
              </div>
              <div style={tipStyle}>
                  <p>Please click to select letters to build word</p>
              </div>
              <br/>
          </div>
          <div style={resultStyle} align="center">
              <p>Your Score: {totalScore}</p>
              <p>Your valid words:</p>
              <ul>{wordList}</ul>
          </div>

      </React.Fragment>
    );
  }
}

const structuredSelector = createStructuredSelector({
  gameBoard: state => state.gameBoard,
    selectedCells: state => state.selectedCells,
    currentWord: state => state.currentWord,
    totalScore: state => state.totalScore,
    allWords: state => state.allWords,
    start: state => state.start

});

const mapDispatchToProps = {startGame, submitWord, clearWord, addLetter}

export default connect(structuredSelector, mapDispatchToProps)(BoggleGame)
