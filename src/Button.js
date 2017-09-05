import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import request2Api from './request2Api'

class Button extends Component {
  constructor(props) {
    super(props);
    this.onClick = this.onClick.bind(this);
  }

  onClick(event) {
      request2Api(this.props.label);
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
