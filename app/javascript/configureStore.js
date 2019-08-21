import {createStore, applyMiddleware} from "redux";
import thunk from "redux-thunk";

const initialState = {
    gameBoard: [
        [{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true}],
        [{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true}],
        [{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true}],
        [{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true},{letter: '?', selected: true}]
    ],
    selectedCells: [],
    currentWord: [],
    totalScore: 0,
    allWords: [],
    start: false


};

function rootReducer(state, action){
    console.log(action.type);
    switch(action.type){
        case "START_GAME_SUCCESS":
            return {gameBoard: action.json.gameBoard,
                    selectedCells: [],
                    currentWord: [],
                    totalScore: 0,
                    allWords: [],
                    start: true
                    };
        case "SUBMIT_WORD_SUCCESS":
            let word = state.currentWord
            let score = 0;

            let len = word.length;

            if (len < 3) {
                score = 0
            } else if (len == 3 || len == 4) {
                score = 1;
            } else if (len == 5) {
                score = 2;
            } else if (len == 6) {
                score = 3;
            } else if (len == 7) {
                score = 5;
            } else {
                score = 11;
            }

            state.allWords.push(word.join(""));

            for(let i = 0; i < state.gameBoard.length; ++ i){
                for(let j = 0; j < state.gameBoard[0].length; ++ j){
                    state.gameBoard[i][j].selected = false;
                }
            }
            return {gameBoard: state.gameBoard,
                selectedCells: [],
                currentWord: [],
                totalScore: state.totalScore + score ,
                allWords: state.allWords,
                start: true
            };
        case "CLEAR_WORD_SUCCESS":
            for(let i = 0; i < state.gameBoard.length; ++ i){
                for(let j = 0; j < state.gameBoard[0].length; ++ j){
                    state.gameBoard[i][j].selected = false;
                }
            }
            return {gameBoard: state.gameBoard,
                selectedCells: [],
                currentWord: [],
                totalScore: state.totalScore ,
                allWords: state.allWords,
                start: true
            };

        case "ADD_LETTER_SUCCESS":
            //TODO: not sure why directly assigning state.currentWord to currentWord does not cause the state change.
            let temp = [];
            for(let index = 0; index < state.currentWord.length; ++ index){
                temp[index] = state.currentWord[index]
            }
            temp.push(action.json.letter)
            state.selectedCells.push({i: action.json.i, j: action.json.j});
            state.gameBoard[action.json.i][action.json.j].selected = true;
            return {gameBoard: state.gameBoard,
                selectedCells: state.selectedCells,
                currentWord: temp,
                totalScore: state.totalScore,
                allWords: state.allWords,
                start: true
            };
        case "SUBMIT_WORD_FAILED":
            let message = action.json.message;
            alert(message);
            for(let i = 0; i < state.gameBoard.length; ++ i){
                for(let j = 0; j < state.gameBoard[0].length; ++ j){
                    state.gameBoard[i][j].selected = false;
                }
            }
            return {gameBoard: state.gameBoard,
                selectedCells: [],
                currentWord: [],
                totalScore: state.totalScore ,
                allWords: state.allWords,
                start: true
            };

    }
    return state;
}



export  default function configureStore() {
    const store = createStore(
        rootReducer,
        initialState,
        applyMiddleware(thunk));
    return store;
}