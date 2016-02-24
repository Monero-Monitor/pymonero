import requests as req
import json
from . import classes

def unitsToCoins(units):
    return units / 1000000000000.0

# getWalletBalance() :: Function that returns "get_info" rpc call info
def getWalletBalance(wallet):
    
    # Create rpc data input
    rpc_input = { "method": "getbalance" }       # simplewallet rpc method
    rpc_input.update(wallet.RPC_STANDARD_VALUES) # add standard rpc values
    
    # Execute the rpc request and store response output
    resp = req.post(wallet.RPC_URL,data=json.dumps(rpc_input),headers=wallet.RPC_STANDARD_HEADER)
    output = resp.json()
    
    if not "result" in output:
        errormsg = "getWalletBalance: 'result' not found in reply."
        print(errormsg)
        raise RuntimeError(errormsg)
        return
    
    # Organize rpc response output and return
    balance = classes.WalletBalance(output["result"])
    return balance
