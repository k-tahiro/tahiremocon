function request2Api(resource) {
  const a = resource.split('_')
  const request = new Request('/bto_ir_cmd/transmit', {
    method: 'POST',
    headers: new Headers({
      'Content-Type': 'application/json'
    }),
    body: JSON.stringify({
      'mode': a[0],
      'degree': Number(a[1])
    })
  });
  return fetch(request).then(response => {
    if(response.status === 200) return response.json();
    else throw new Error('Something went wrong on api server!');
  })
}

export default request2Api;
