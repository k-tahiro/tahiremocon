import React from 'react';

function RemoconStatus(props) {
  return <div className="RemoconStatus">
    {(() => {
      if (props.success === undefined) {
        return ''
      } else if (props.success === true) {
        return `${props.label}成功`
      } else {
        return `${props.label}失敗`
      }
    })()}
  </div>
}

export default RemoconStatus;
