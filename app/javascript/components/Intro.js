import React from "react"
import { withRouter } from 'react-router-dom';
import Styles from "./Styles"

class Intro extends React.Component {
    constructor() {
        super();
        this.routeChange = this.routeChange.bind(this);
    }

    routeChange() {
        let path = `/boggle`;
        this.props.history.push(path);
    }
    render() {
        return(
            <React.Fragment>
                <div align="center">
                    <h1>Boggle Game Design</h1>
                </div>
                <p><b>Current word</b></p>
                <p>The design of this <a href="https://en.wikipedia.org/wiki/Boggle">Boggle Game</a> includes two parts: Ruby on Rails backend server and React Redux frontend client.
                </p>
                <p>The backend server contains two REST endpoints: one generates a 4x4 matrix of random characters, and the other performs words validation by calling an external API.
                </p>
                <p>The frontend code allows players interacting with the game by:</p>
                <ul>
                    <li>Starting a new game</li>
                    <li>Selecting letters to build words. Instead of providing an input text box for players enter words, this game is designed to be more interactive by having clickable buttons at
                        each matrix's cells. Since letters at each cell can be used at most once for each word, the buttons will be toggled to be disabled after being clicked.</li>
                    <li>Submitting words to server for validation</li>
                    <li>Clearing word</li>
                </ul>
                    Players earn points for submitting valid words (see <a href="https://en.wikipedia.org/wiki/Boggle">Boggle Game</a> for more details.)  The longer the word, the more points can be earned.  The list of valid words submitted by players will be displayed


                <p><b>Future Enhancements</b></p>
                <ul>
                    <li>The game is currently designed for single player. It can be enhanced for a group of players </li>
                    <li>As mentioned above, the word validation function is handled by the server side. This will generate a lot of
                    traffic and consume a lot of resource (threads) on the server as the number of players grows. This issue can be avoid by allowing client code to call external API
                    to validate the word.</li>
                    <li>Since the matrix are filled with random letters, there are always a lot more consonants than vowels (ratio of 4:1) on the matrix.
                        This limits the number of words can be built since average English words have the ratio between 1:1 and 2:1.
                        We should come up a better logic to improve this ratio.
                    </li>
                </ul>


                <div align="center">
                    <button onClick={this.routeChange} style={Styles.startButton}>Enter Boggle Game</button>
                </div>
            </React.Fragment>
        )

    }
}

export default withRouter(Intro);