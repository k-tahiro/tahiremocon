import React, { Component } from 'react';
import loadCmd from './loadCmd'
import Button from './Button';

class ButtonList extends Component {
  constructor(props) {
    super(props)
    this.state = {}
    loadCmd().then(json => {
      this.setState({list: json})
    })
  }

  render() {
    return (
      <div className="ButtonList">
        {
          (() => {
            if ('list' in this.state && this.state.list.length) {
              return this.state.list.map(
                cmd => <Button
                           key={cmd}
                           label={cmd}
                           handleClick={this.props.handleClick}
                       />
              );
            }
          })()
        }
      </div>
    )
  }
}

export default ButtonList;
