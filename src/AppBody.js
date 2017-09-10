import React, { Component } from 'react';
import RemoconStatus from './RemoconStatus';
import ButtonList from './ButtonList';
import request2Api from './request2Api'

class AppBody extends Component {
  constructor(props) {
    super(props)
    this.state = {
      label: undefined,
      success: undefined
    }
    this.handleClick = this.handleClick.bind(this)
  }

  handleClick(label) {
    request2Api(label).then(obj => {
      if (obj.success) this.setState({label, success: true});
      else this.setState({label, success: false})
    }, e => {
      this.setState({label, success: false})
    })
  }

  render() {
    return (
      <div className="AppBody">
        <RemoconStatus label={this.state.label} success={this.state.success} />
        <ButtonList handleClick={this.handleClick} />
      </div>
    )
  }
}

export default AppBody;
