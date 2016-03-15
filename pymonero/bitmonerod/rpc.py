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
            return result
        else:
            error = utils.ErrorMessage(output["error"]["message"])
            return error
    except:
        error = utils.ErrorMessage("Error returning result from 'daemonJSONrpc'.")
        return error

def daemonRPC(daemon, interface, rpc_input):
    '''daemonRPC() :: Send daemon RPC method and process initial result.'''
    
    method_url = daemon.URL + interface
    
    # Execute the rpc request and return response output
    try:
        resp = req.post(method_url,data=json.dumps(rpc_input),headers=daemon.RPC_STANDARD_HEADER)
        output = resp.json()
        
        return output
    except:
        error = utils.ErrorMessage("Error returning result from 'daemonRPC'.")
        return error

def getDaemonInfo(daemon):
    ''' getDaemonInfo() :: Function that returns "get_info" rpc call info. '''
    
    # Create rpc data input
    rpc_input = {"method": "get_info"}
    result = daemonJSONrpc(daemon, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(result, 'error'):
        return result
    
    # Return formatted result
    try:
        info = classes.DaemonInfo(result)
        return info
    except:
        error = utils.ErrorMessage("Error parsing result as class DaemonInfo.")
        return error

def getConnections(daemon):
    '''getConnections() :: Function that returns "get_connections" rpc call info.'''
    
    # Create rpc data input
    rpc_input = {"method": "get_connections"}
    result = daemonJSONrpc(daemon, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(result, 'error'):
        return result
    
    # Return formatted result
    try:
        connections = classes.Connections(result)
        return connections
    except:
        error = utils.ErrorMessage("Error parsing result as class Connections.")
        return error

def hardForkInfo(daemon):
    ''' hardForkInfo() :: Function that returns "hard_fork_info" rpc call info. '''
    
    # Create rpc data input
    rpc_input = {"method": "hard_fork_info"}
    result = daemonJSONrpc(daemon, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(result, 'error'):
        return result
    
    # Return formatted result
    try:
        hard_fork_info = classes.HardForkInfo(result)
        return hard_fork_info
    except:
        error = utils.ErrorMessage("Error parsing result as 'HardForkInfo'.")
        return error

def getBlockCount(daemon):
    ''' getBlockCount() :: Function that returns "getblockcount" rpc call info. '''
    
    # Create rpc data input
    rpc_input = {"method": "getblockcount"}
    result = daemonJSONrpc(daemon, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(result, 'error'):
        return result
    
    # Return formatted result
    try:
        count = int(result["count"])
        return count
    except:
        error = utils.ErrorMessage("Error parsing result as block count type int.")
        return error

def getTransactions(daemon,hashes,block=None):
    ''' getDaemonInfo(hashes,[block]) :: Function that returns "get_info" rpc call info. '''
    
    # RPC method
    method = "/gettransactions"
    
    # Create bitmonerod rpc method input
    if isinstance(hashes, str):
        txs_hashes = [ hashes ]
    else:
        txs_hashes = hashes
    
    rpc_input = {"txs_hashes": txs_hashes, "decode_as_json": True}
    output = daemonRPC(daemon, method, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(output, 'error'):
        return output
    
    if "txs_as_json" in output:
        txs_as_json = output["txs_as_json"]
    else:
        txs_as_json = []
    
    if "missed_tx" in output:
        missed_tx = output["missed_tx"]
    else:
        missed_tx = []
    
    if len(txs_hashes) != (len(txs_as_json) + len(missed_tx)):
        error = utils.ErrorMessage("There was an unknown error returning txs. Number returned != number input.")
        return error
    
    try:
        transactions = classes.Transactions(hashes, txs_as_json, missed_tx, block)
        return transactions
    except:
        error = utils.ErrorMessage("Error parsing result as class Transactions.")
        return error

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
            return error
    
        # Gather block header:
        block_header = result["block_header"]
        
        # Gather block details:
        output_json_str = str(output["result"]["json"])
        output_json_str.replace('\\', '')
        output_json = json.loads(output_json_str)
        
        # Get block info
        blockInfo = classes.BlockInfo(block_header, output_json)
        
        # Return block info
        return blockInfo
        
    except:
        error = utils.ErrorMessage("Error parsing result as class BlockInfo.")
        return error

def getBlockByHeight(daemon,block_height):
    ''' getBlockByHeight(block_height) :: Function that returns "getblock" rpc call info
        with "height" param. '''
    
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = { "method": "getblock", "params": { "height": block_height } }
    
        # Get block and parse into structure
        blockInfo = _getBlockAndParse(daemon,rpc_input)
        
        # Return block info
        return blockInfo
    else:
        error = utils.ErrorMessage('Block height' + str(block_height) + 'is invalid: not an integer.')
        return error

def getBlockByHash(daemon,block_hash):
    ''' getBlockByHash(block_hash) :: Function that returns "getblock" rpc call info with
        "hash" param. '''
    
    # Define bitmonerod rpc method input
    rpc_input = { "method": "getblock", "params": { "hash": block_hash } }
    
    # Get block and parse into structure
    blockInfo = _getBlockAndParse(daemon,rpc_input)
    
    # Return block info
    return blockInfo

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
            return error
        
        # Gather block header:
        block_header = result["block_header"];
        
        # Get block info
        blockHeader = classes.BlockHeader(block_header)
        
        # Return block header info
        return blockHeader
        
    except:
        error = utils.ErrorMessage("Error parsing result as class BlockHeader.")
        return error

def getBlockHeaderByHeight(daemon,block_height):
    ''' getBlockHeaderByHeight(block_height) :: Function that returns
        "getblockheaderbyheight" rpc call info with "height" param. '''
    
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = {"method": "getblockheaderbyheight", "params": {"height": block_height}}
        
        # Get block and parse into structure
        blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
        # Return block header info
        return blockHeader
    else:
        error = utils.ErrorMessage('Block height' + str(block_height) + 'is invalid: not an integer.')
        return error

def getBlockHeaderByHash(daemon,block_hash):
    ''' getBlockHeaderByHash(block_hash) :: Function that returns "getblockheaderbyheight"
        rpc call info with "hash" param. '''
    
    if isinstance(block_hash, str):
        # Define bitmonerod rpc method input
        rpc_input = {"method": "getblockheaderbyhash", "params": {"hash": block_hash}}
        
        # Get block and parse into structure
        blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
        # Return block header info
        return blockHeader
    else:
        error = utils.ErrorMessage('Block hash' + str(block_hash) + 'is invalid: not a string.')
        return error

def getLastBlockHeader(daemon):
    ''' getLastBlockHeader() :: Function that returns "getlastblockheader" rpc call info. '''
    
    # Define bitmonerod rpc method input
    rpc_input = {"method": "getlastblockheader"}
    
    # Get block and parse into structure
    blockHeader = _getBlockHeaderAndParse(daemon,rpc_input)
    
    # Return daemon info
    return blockHeader

def getBlockHash(daemon, block_height):
    ''' getBlockHash(block_height) :: Function that returns "on_getblockhash" rpc call info. '''
    
    if isinstance(block_height, int):
        # Define bitmonerod rpc method input
        rpc_input = {"method": "on_getblockhash", "params": [block_height]}
        blockHash = daemonJSONrpc(daemon, rpc_input)
        
        # Return formatted result (valid result is just a string of the hash).
        return blockHash
    
    else:
        error = utils.ErrorMessage('Block height' + str(block_height) + 'is invalid: not an int.')
        return error

def getBlockTemplate(daemon, wallet_address, reserve_size):
    ''' getDaemonInfo(wallet_address, reserve_size) :: Function that returns
        "getblocktemplate" rpc call info. '''
    
    # Create rpc data input
    rpc_input = {"method": "getblocktemplate",
                 "params": {"wallet_address": wallet_address, "reserve_size": reserve_size}}
    result = daemonJSONrpc(daemon, rpc_input)
    
    # Check if bitmonerod gave a specific error message
    if hasattr(result, 'error'):
        return result
    
    # Return formatted result
    try:
        info = classes.BlockTemplate(result)
        return info
    except:
        error = utils.ErrorMessage("Error parsing result as class 'BlockTemplate'.")
        return error
