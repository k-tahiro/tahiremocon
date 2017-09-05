import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';

class Button extends Component {
  constructor(props) {
    super(props)
    this.onClick = this.onClick.bind(this)
  }

  onClick(e) {
    this.props.handleClick(this.props.label)
  }

  render() {
    return (
      <RaisedButton
        label={this.props.label}
        onClick={this.onClick}
      />
    )
  }
}

export default Button;
