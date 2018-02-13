var jayson = require('jayson');

// Create a client connected to backend server
var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

// Test RPC method
// 异步，后端返回结果后，才会调用callback
// callback参数，err是网络有问题，error是类似404的错误，response是正常返回的内容
function add(a, b, callback) {
    client.request('add', [a, b], function(err, error, response) {
        if (err) throw err;
        console.log(response);
        callback(response);
    });
}


module.exports = {
    add : add,
};
