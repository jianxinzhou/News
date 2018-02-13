var client = require('./rpc_client');

// test 'add' rpc method
client.add(1, 2, function(response) {
    console.assert(response == 3)
});
