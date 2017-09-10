function request2Api(resource) {
  const request = new Request(`/bto_ir_cmd/${resource}`);
  return fetch(request).then(response => {
    if(response.status === 200) return response.json();
    else throw new Error('Something went wrong on api server!');
  })
}

export default request2Api;
