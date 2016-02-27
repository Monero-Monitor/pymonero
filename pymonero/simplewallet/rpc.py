import requests as req
import json
from . import classes
from .. import utils

def walletJSONrpc(wallet, rpc_input):
    ''' walletJSONrpc() :: Send wallet JSON_RPC method and process initial result. '''
    
    # Add standard rpc values
    rpc_input.update(wallet.RPC_STANDARD_VALUES)
    
    # Execute the rpc request and return response output
    try:
        resp = req.post(wallet.RPC_URL,data=json.dumps(rpc_input),headers=wallet.RPC_STANDARD_HEADER)
        output = resp.json()
        
        # Return result or error message from rpc call
        if "result" in output:
            result = output["result"]
            return result, 0
        else:
            error = utils.ErrorMessage(output["error"]["message"])
            code = output["error"]["code"]
            return error, code
    except:
        result = utils.ErrorMessage("Error returning result fom 'walletJSONrpc'.")
        return result, 1

def getWalletBalance(wallet):
    ''' getWalletBalance() :: Function that returns "getbalance" rpc call info. '''

    # Create rpc data input
    rpc_input = { "method": "getbalance" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            wallet_balance = classes.WalletBalance(result)
            return wallet_balance, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'getWalletBalance'.")
            return error, 1
    else:
        return result, err

def getWalletAddress(wallet):
    ''' getWalletAddress() :: Function that returns "getaddress" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "getaddress" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            address = result["address"]
            return address, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'getWalletAddress'.")
            return error, 1
    else:
        return result, err

def getWalletHeight(wallet):
    ''' getWalletHeight() :: Function that returns "getheight" rpc call info. '''
    
    # Create rpc data input
    rpc_input = { "method": "getheight" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            return result["height"], 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'getWalletHeight'.")
            return error, 1
    else:
        return result, err

def getPayments(wallet,payment_id):
    ''' getPayments() :: Returns payments to wallet matching payment_id using "get_payments" rpc call. '''
    
    # Create rpc data input
    rpc_input = { "method": "get_payments", "params": {"payment_id": payment_id} }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            payments = []
            for i in range(0, len(result["payments"])):
                payments.append(classes.Payment(result["payments"][i]))
            return payments, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'getWalletHeight'.")
            return error, 1
    else:
        return result, err

def getBulkPayments(wallet,pay_ids):
    ''' getPayments() :: Returns payments to wallet matching payment_id using "get_payments" rpc call. 
          "pay_ids" can either be a single payment ID string, or an array of payment ID strings.
          This method is preferred over the getPayments() option. '''
    
    # Make sure payment_ids is an array
    if isinstance(pay_ids, str):
        payment_ids = [ pay_ids ]
    else:
        payment_ids = hashes
    
    # Create rpc data input
    rpc_input = { "method": "get_bulk_payments", "params": {"payment_ids": payment_ids} }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            payments = []
            for i in range(0, len(result["payments"])):
                payments.append(classes.Payment(result["payments"][i]))
            return payments, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'getWalletHeight'.")
            return error, 1
    else:
        return result, err

def makeTransfer(wallet, receive_addresses, amounts_atomic, payment_id, mixin):
    ''' makeTransfer() :: Make transaction(s) (Note: 1 Coin = 1e12 atomic units). '''
    
    # Prep destinations rpc array
    destinations, err = _setupDestinations(receive_addresses, amounts_atomic)
    if err != 0:
        return destinations, err
    
    # Create rpc data input
    params = { "destinations": destinations, "mixin": mixin, "payment_id": payment_id}
    rpc_input = { "method": "transfer", "params": params }
    
    print(json.dumps(rpc_input, indent=2))
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            transfer_result = classes.TransferResult(result)
            return transfer_result, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'makeTransfer'.")
            return error, 1
    else:
        return result, err

def _setupDestinations(receive_addresses, amounts_atomic):
    ''' _setupDestination :: Put receive_addresses and amounts_atomic into destinations array '''

    # Make sure receive_addresses is an array
    if isinstance(receive_addresses, str):
        recipients = [ receive_addresses ]
    else:
        recipients = receive_addresses
    
    # Make sure amounts_atomic is an array
    if isinstance(amounts_atomic, int):
        amounts = [ amounts_atomic ]
    else:
        amounts = amounts_atomic
    
    # Make sure number of recipients matches number of amounts
    N_recipients = len(recipients)
    if N_recipients != len(amounts):
        error = utils.ErrorMessage("Error: Number of recipients does not match number of amounts.")
        return error, 1
    
    # Fill out destinations for rpc data input
    destinations = []
    for i in range(0, N_recipients):
        destinations.append({"address": recipients[i], "amount": amounts[i]})
    
    return destinations, 0
    