import React, { Component } from 'react';
import Button from './Button';
import request2Api from './request2Api'

class ButtonList extends Component {
  constructor(props) {
    super(props)
    this.state = {
      success: undefined,
      label: undefined
    }
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(label) {
    let success = undefined;
    try {
      request2Api(label);
      success = true;
    }
    catch(e) {
      success = false;
    }
    this.setState({
      success,
      label
    });
  }

  render() {
    return (
      <div>
        {
          (() => {
            if (this.state.success === undefined) {
              return <div className="Status"></div>
            } else if (this.state.success === true) {
              return <div className="Status">{this.state.label}成功</div>
            } else {
              return <div className="Status">{this.state.label}失敗</div>
            }
          })()
        }
        <Button
          label="Default"
          handleClick={this.handleClick}
        />
      </div>
    )
  }
}

export default ButtonList;
