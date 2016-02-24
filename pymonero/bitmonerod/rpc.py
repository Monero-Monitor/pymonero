import requests as req
import json
from . import classes

# getDaemonInfo() :: Function that returns "get_info" rpc call info
def getDaemonInfo(daemon):

    # Create rpc data input
    rpc_input = { "method": "get_info" }         # bitmonerod rpc method
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values
    
    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "result" in output:
        errormsg = "getDaemonInfo: 'result' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
    
    # Organize rpc response output and return
    info = classes.DaemonInfo(output["result"])
    return info

# getConnections() :: Function that returns "get_connections" rpc call info
def getConnections(daemon):

    # Create rpc data input
    rpc_input = { "method": "get_connections" }  # bitmonerod rpc method
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values

    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "result" in output:
        errormsg = "getConnections: 'result' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
    
    # Organize rpc response output and return
    connections = classes.Connections(output["result"])
    return connections

# hardForkInfo() :: Function that returns "hard_fork_info" rpc call info
def hardForkInfo(daemon):

    # Create rpc data input
    rpc_input = { "method": "hard_fork_info" }  # bitmonerod rpc method
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values

    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "result" in output:
        errormsg = "getBlockCount: 'result' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
        
    hard_fork_info = classes.HardForkInfo(output["result"])
    return hard_fork_info

# getBlockCount() :: Function that returns "getblockcount" rpc call info
def getBlockCount(daemon):

    # Create rpc data input
    rpc_input = { "method": "getblockcount" }  # bitmonerod rpc method
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values

    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "result" in output:
        errormsg = "getBlockCount: 'result' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
    
    if output["result"]["status"] != "OK":
        errormsg = "getBlockCount: Status not OK"
        print(errormsg)
        return 0
    else:
        count = output["result"]["count"]
        return count
        
# getDaemonInfo() :: Function that returns "get_info" rpc call info
def getTransactions(daemon,hashes,block=None):
    
    # bitmonerod url
    url = daemon.URL + "/gettransactions"
    
    if isinstance(hashes, str):
        txs_hashes = [ hashes ]
    else:
        txs_hashes = hashes
    # Create bitmonerod rpc method input
    rpc_input = { "txs_hashes": txs_hashes, "decode_as_json": True }

    # Execute the rpc request and store response output
    resp = req.post(url,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "txs_as_json" in output:
        errormsg = "getTransactions: 'txs_as_json' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
    
    # Organize rpc response output and return
    txs_as_json = output["txs_as_json"]
    n_txs = len(txs_as_json)
    transactions = []
    for i in range(0,n_txs):
        output_json_str = str(txs_as_json[i])
        output_json_str.replace('\\', '')
        output_json = json.loads(output_json_str)
        transactions.append(classes.Transaction(hashes[i], output_json, block))
    return transactions

# _getBlockAndParse(rpc_input) :: Function called by getBlockByHash & getBlockByHeight to return block info
def _getBlockAndParse(daemon,rpc_input):
    
    # Add standard rpc values to input
    rpc_input.update(daemon.RPC_STANDARD_VALUES)
    
    # Execute the rpc request
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    
    # Rpc response output
    output = json.loads( "\n".join(filter(lambda l: "blob" not in l, resp.text.split("\n"))))
    
    if not "result" in output:
        return 1
    
    # Gather block header:
    block_header = output["result"]["block_header"];
    
    # Gather block details:
    output_json_str = str(output["result"]["json"])
    output_json_str.replace('\\', '')
    output_json = json.loads(output_json_str)
    
    # Get block info
    blockInfo = classes.BlockInfo(block_header, output_json)
    
    # Return daemon info
    return blockInfo

# getBlockByHeight(block_height) :: Function that returns "getblock" rpc call info with "height" param
def getBlockByHeight(daemon,block_height):
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getblock", "params": { "height": block_height } }
    
    # Get block and parse into structure
    blockInfo = _getBlockAndParse(daemon,rpc_input)
    
    if blockInfo == 1:
        errormsg = "getBlockByHeight: 'result' not found in reply (in '_getBlockAndParse')."
        print(errormsg)
        raise RuntimeError(errormsg)
    
    # Return daemon info
    return blockInfo

# getBlockByHash() :: Function that returns "getblock" rpc call info with "hash" param
def getBlockByHash(daemon,block_hash):
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getblock", "params": { "hash": block_hash } }
    
    # Get block and parse into structure
    blockInfo = _getBlockAndParse(daemon,rpc_input)
    
    if blockInfo == 1:
        errormsg = "getBlockByHash: 'result' not found in reply (in '_getBlockAndParse')."
        print(errormsg)
        raise RuntimeError(errormsg)
    
    # Return daemon info
    return blockInfo

# _getBlockAndParse(rpc_input) :: Function called by getBlockByHash & getBlockByHeight to return block info
def _getBlockHeaderAndParse(daemon,rpc_input):
    
    # Add standard rpc values to input
    rpc_input.update(daemon.RPC_STANDARD_VALUES)
    
    # Execute the rpc request
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    
    # Rpc response output
    output = json.loads( "\n".join(filter(lambda l: "blob" not in l, resp.text.split("\n"))))
    
    # Gather block header:
    block_header = output["result"]["block_header"];
    
    # Get block info
    blockHeader = classes.BlockHeader(block_header)
    
    # Return daemon info
    return blockHeader

# getBlockHeaderByHeight(block_height) :: Function that returns "getblock" rpc call info with "height" param
def getBlockHeaderByHeight(daemon,block_height):
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = { "method": "getblockheaderbyheight", "params": { "height": block_height } }
        
        # Get block and parse into structure
        blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
        # Return daemon info
        return blockHeader
    else:
        print('Block height' + str(block_height) + 'is invalid: not an integer.')

# getBlockHeaderByHash() :: Function that returns "getblock" rpc call info with "hash" param
def getBlockHeaderByHash(daemon,block_hash):
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getblockheaderbyhash", "params": { "hash": block_hash } }
    
    # Get block and parse into structure
    blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
    # Return daemon info
    return blockHeader
    
# getBlockHeaderByHash() :: Function that returns "getblock" rpc call info with "hash" param
def getLastBlockHeader(daemon):
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getlastblockheader" }
    
    # Get block and parse into structure
    blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
    # Return daemon info
    return blockHeader

# getBlockHash() :: Function that returns "on_getblockhash" rpc call info
def getBlockHash(daemon, block_height):
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "on_getblockhash", "params": [ block_height ] }
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values
    
    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    #hash = { "hash": output["result"], "height": block_height }
    hash = output["result"]
    return hash

# getDaemonInfo() :: Function that returns "getblocktemplate" rpc call info
def getBlockTemplate(daemon, wallet_address, reserve_size):

    # Create rpc data input
    rpc_input = { "method": "getblocktemplate", 
                    "params": { "wallet_address": wallet_address, "reserve_size": reserve_size }
                } # bitmonerod rpc method
    rpc_input.update(daemon.RPC_STANDARD_VALUES) # add standard rpc values
    
    # Execute the rpc request and store response output
    resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
    output = resp.json()
    
    # Organize rpc response output and return
    info = classes.BlockTemplate(output["result"])
    return info
