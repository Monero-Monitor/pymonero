import requests as req
import json
from . import classes
from .. import utils

def daemonJSONrpc(daemon, rpc_input):
    '''daemonJSONrpc() :: Send daemon JSON_RPC method and process initial result.'''
    
    # Add standard rpc values
    rpc_input.update(daemon.RPC_STANDARD_VALUES)
    
    # Execute the rpc request and return response output
    try:
        resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
        output = resp.json()
        
        # Return result or error message from rpc call
        if "result" in output:
            result = output["result"]
            return result, 0
        else:
            error = utils.ErrorMessage(output["error"]["message"])
            code = output["error"]["code"]
            if code == 0:
                code = -1
            return error, code
    except:
        result = utils.ErrorMessage("Error returning result from 'daemonJSONrpc'.")
        return result, 1

def daemonRPC(daemon, interface, rpc_input):
    '''daemonRPC() :: Send daemon RPC method and process initial result.'''
    
    method_url = daemon.URL + interface
    
    # Execute the rpc request and return response output
    try:
        resp = req.post(method_url,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
        output = resp.json()
        
        return output, 0
    except:
        error = utils.ErrorMessage("Error returning result from 'daemonRPC'.")
        return error, 1

def getDaemonInfo(daemon):
    ''' getDaemonInfo() :: Function that returns "get_info" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "get_info" } # Get RPC result
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            info = classes.DaemonInfo(result)
            return info, 0
        except:
            error = utils.ErrorMessage("Error returning result from 'getDaemonInfo'.")
            return error, 1
    else:
        return result, err

def getConnections(daemon):
    '''getConnections() :: Function that returns "get_connections" rpc call info.'''
    
    # Create rpc data input
    rpc_input = { "method": "get_connections" } # Get RPC result
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            connections = classes.Connections(result)
            return connections, 0
        except:
            error = utils.ErrorMessage("Error returning result from 'getConnections'.")
            return error, 1
    else:
        return result, err

def hardForkInfo(daemon):
    ''' hardForkInfo() :: Function that returns "hard_fork_info" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "hard_fork_info" } # Get RPC result
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            hard_fork_info = classes.HardForkInfo(result)
            return hard_fork_info, 0
        except:
            error = utils.ErrorMessage("Error returning result from 'hardForkInfo'.")
            return error, 1
    else:
        return result, err

def getBlockCount(daemon):
    ''' getBlockCount() :: Function that returns "getblockcount" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "getblockcount" } # Get RPC result
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            count = int(result["count"])
            return count, 0
        except:
            error = utils.ErrorMessage("Error returning result from 'getBlockCount'.")
            return error, 1
    else:
        return result, err

def getTransactions(daemon,hashes,block=None):
    ''' getDaemonInfo(hashes,[block]) :: Function that returns "get_info" rpc call info. '''
    
    # RPC method
    method = "/gettransactions"
    
    # Create bitmonerod rpc method input
    if isinstance(hashes, str):
        txs_hashes = [ hashes ]
    else:
        txs_hashes = hashes
    rpc_input = { "txs_hashes": txs_hashes, "decode_as_json": True }
    
    output, err = daemonRPC(daemon, method, rpc_input)
    
    if err == 0:
        if "missed_tx" in output:
            error = utils.ErrorMessage("Error returning result from 'getTransactions': missed_tx")
            error.missed_tx = output["missed_tx"]
            return error, -1
        else:
            try:
                txs_as_json = output["txs_as_json"]
                n_txs = len(txs_as_json)
                transactions = []
                for i in range(0,n_txs):
                    output_json_str = str(txs_as_json[i])
                    output_json_str.replace('\\', '')
                    output_json = json.loads(output_json_str)
                    transactions.append(classes.Transaction(hashes[i], output_json, block))
                return transactions, 0
            except:
                print(json.dumps(output, indent=2))
                error = utils.ErrorMessage("Error returning result from 'getTransactions'.")
                return error, 1
    else:
        return output, err

def _getBlockAndParse(daemon,rpc_input):
    ''' _getBlockAndParse(rpc_input) :: Function called by getBlockByHash &
        getBlockByHeight to return block info. There is some weird stuff going on with
        block information that prevents being about to use the standard daemonJSONrpc()
        function. '''
    
    # Add standard rpc values to input
    rpc_input.update(daemon.RPC_STANDARD_VALUES)
    
    try:
        # Execute the rpc request
        resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
        
        # Rpc response output
        output = json.loads( "\n".join(filter(lambda l: "blob" not in l, resp.text.split("\n"))))
        
        if "result" in output:
            result = output["result"]
        else:
            error = utils.ErrorMessage(output["error"]["message"])
            code = output["error"]["code"]
            if code == 0:
                code = -1
            return error, code
        
    except:
        error = utils.ErrorMessage("Error returning result from '_getBlockAndParse'.")
        return error, 1
    
    try:
        # Gather block header:
        block_header = result["block_header"]
        
        # Gather block details:
        output_json_str = str(output["result"]["json"])
        output_json_str.replace('\\', '')
        output_json = json.loads(output_json_str)
        
        # Get block info
        blockInfo = classes.BlockInfo(block_header, output_json)
        
        # Return daemon info
        return blockInfo, 0
    except:
        error = utils.ErrorMessage("Error returning block info from '_getBlockAndParse'.")
        return error, 1

def getBlockByHeight(daemon,block_height):
    ''' getBlockByHeight(block_height) :: Function that returns "getblock" rpc call info
        with "height" param. '''
    
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = { "method": "getblock", "params": { "height": block_height } }
    
        # Get block and parse into structure
        blockInfo, err = _getBlockAndParse(daemon,rpc_input)
        
        # Return daemon info
        return blockInfo, err
    else:
        error = utils.ErrorMessage('Block height' + str(block_height) + 'is invalid: not an integer.')
        return error, 1

def getBlockByHash(daemon,block_hash):
    ''' getBlockByHash(block_hash) :: Function that returns "getblock" rpc call info with
        "hash" param. '''
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getblock", "params": { "hash": block_hash } }
    
    # Get block and parse into structure
    blockInfo, err = _getBlockAndParse(daemon,rpc_input)
    
    # Return daemon info
    return blockInfo, err

def _getBlockHeaderAndParse(daemon,rpc_input):
    ''' _getBlockAndParse(rpc_input) :: Function called by getBlockByHash &
        getBlockByHeight to return block info. '''
    
    # Add standard rpc values to input
    rpc_input.update(daemon.RPC_STANDARD_VALUES)
    
    try:
        # Execute the rpc request
        resp = req.post(daemon.RPC_URL,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
        
        # Rpc response output
        output = json.loads( "\n".join(filter(lambda l: "blob" not in l, resp.text.split("\n"))))
        
        if "result" in output:
            result = output["result"]
        else:
            error = utils.ErrorMessage(output["error"]["message"])
            code = output["error"]["code"]
            if code == 0:
                code = -1
            return error, code
        
    except:
        error = utils.ErrorMessage("Error returning result from '_getBlockHeaderAndParse'.")
        return error, 1
    
    try:
        # Gather block header:
        block_header = result["block_header"];
        
        # Get block info
        blockHeader = classes.BlockHeader(block_header)
        
        # Return daemon info
        return blockHeader, 0
    except:
        error = utils.ErrorMessage("Error returning header info from '_getBlockHeaderAndParse'.")
        return error, 1

def getBlockHeaderByHeight(daemon,block_height):
    ''' getBlockHeaderByHeight(block_height) :: Function that returns
        "getblockheaderbyheight" rpc call info with "height" param. '''
    
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = { "method": "getblockheaderbyheight", "params": { "height": block_height } }
        
        # Get block and parse into structure
        blockHeader, err = _getBlockHeaderAndParse(daemon,rpc_input)
    
        # Return daemon info
        return blockHeader, err
    else:
        error = utils.ErrorMessage('Block height' + str(block_height) + 'is invalid: not an integer.')
        return error, 1

def getBlockHeaderByHash(daemon,block_hash):
    ''' getBlockHeaderByHash(block_hash) :: Function that returns "getblockheaderbyheight"
        rpc call info with "hash" param. '''
    
    if isinstance(block_hash, str):
        # Define bitmonerod rpc method input
        rpc_input = { "method": "getblockheaderbyhash", "params": { "hash": block_hash } }
        
        # Get block and parse into structure
        blockHeader, err = _getBlockHeaderAndParse(daemon,rpc_input)
    
        # Return daemon info
        return blockHeader, err
    else:
        error = utils.ErrorMessage('Block hash' + str(block_hash) + 'is invalid: not a string.')
        return error, 1

def getLastBlockHeader(daemon):
    ''' getLastBlockHeader() :: Function that returns "getlastblockheader" rpc call info. '''
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getlastblockheader" }
    
    # Get block and parse into structure
    blockHeader, err = _getBlockHeaderAndParse(daemon,rpc_input)
    
    # Return daemon info
    return blockHeader, err

def getBlockHash(daemon, block_height):
    ''' getBlockHash(block_height) :: Function that returns "on_getblockhash" rpc call info. '''
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "on_getblockhash", "params": [ block_height ] }
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result (valid result is just a string of the hash).
    return result, err
    

def getBlockTemplate(daemon, wallet_address, reserve_size):
    ''' getDaemonInfo(wallet_address, reserve_size) :: Function that returns
        "getblocktemplate" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "getblocktemplate", 
                    "params": { "wallet_address": wallet_address, "reserve_size": reserve_size }
                } # bitmonerod rpc method
    result, err = daemonJSONrpc(daemon, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            info = classes.BlockTemplate(result)
            return info, 0
        except:
            error = utils.ErrorMessage("Error returning result from 'getBlockTemplate'.")
            return error, 1
    else:
        return result, err
