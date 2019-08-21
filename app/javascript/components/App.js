import React from "react"
import {BrowserRouter, Switch, Route} from "react-router-dom"

import {Provider} from 'react-redux'
import BoggleGame from "./BoggleGame";
import Intro from "./Intro";
import configureStore from "../configureStore";
const store = configureStore();
class App extends React.Component {
  render () {
    return (
        <Provider store={store}>
          <BrowserRouter>
            <Switch>
              <Route exact path="/" render={() => <Intro/>}/>

              <Route path="/boggle" render={() => <BoggleGame/>}/>
            </Switch>
          </BrowserRouter>
        </Provider>
    );
  }
}

export default App
