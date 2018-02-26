function loadCmd(callback) {
  const request = new Request('/bto_ir_cmd');
  return fetch(request).then(response => {
    console.log(response);
    if(response.status === 200) return response.json();
    else throw new Error('Something went wrong on api server!');
  })
}

export default loadCmd;
