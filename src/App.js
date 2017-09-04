import React, { Component } from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import logo from './logo.svg';
import './App.css';
import ButtonList from './ButtonList';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>たひリモコン</h2>
        </div>
        <MuiThemeProvider>
          <ButtonList />
        </MuiThemeProvider>
      </div>
    );
  }
}

export default App;
