import json
		
class Daemon:
    def __init__(self, rpchost=None, rpcport=None):
        self.HOST = rpchost if rpchost is not None else 'http://localhost'
        self.PORT = rpcport if rpcport is not None else '18081'
        self.URL                 = self.HOST + ':' + self.PORT
        self.RPC_URL             = self.URL + '/json_rpc'
        self.RPC_STANDARD_HEADER = {'content-type': 'application/json'}
        self.RPC_STANDARD_VALUES = {"jsonrpc": "2.0", "id": "0"}
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)