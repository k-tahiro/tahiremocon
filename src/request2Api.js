const hostname = 'localhost'
const port = 8080
const appname = 'bto_ir_cmd'
const baseUrl = `http://${hostname}:${port}/${appname}`

function request2Api(resource) {
    const request = new Request(`${baseUrl}/${resource}`);
    fetch(request).then(function(response) {
        if(response.status == 200) return response.json();
        else throw new Error('Something went wrong on api server!');
    })
}

export default request2Api;
