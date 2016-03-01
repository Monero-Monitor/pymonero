import requests as req
import json
from . import classes
from .. import utils
import subprocess
import time

def startWallet(wallet, wallet_file, wallet_pass, wallet_name=None):
    ''' startWallet() :: initialize simplewallet for a wallet that already exists. '''
    
    # Setup timer for launching wallet
    start = time.time()
    
    # Trim "http(s)://" from wallet.HOST for simplewallet ip
    wallet_ip = wallet.HOST
    wallet_ip = wallet_ip.replace("http://","")
    wallet_ip = wallet_ip.replace("https://","")
    
    # Create subprocess call for simplewallet in screen
    subprocess_call = ["screen"]
    if wallet_name is not None:
        subprocess_call.extend(["-S", wallet_name])
    subprocess_call.extend(["-dm", "simplewallet",
        "--wallet-file", wallet_file,
        "--password", wallet_pass,
        "--rpc-bind-ip", wallet_ip,
        "--rpc-bind-port", wallet.PORT])
    
    # Call subprocess
    try:
        subprocess.call(subprocess_call)
    except:
        error = utils.ErrorMessage("Error starting simplewallet.")
        return error, 1
    
    err = 1
    k = 0
    while err != 0:
        wallet_balance, err = getWalletHeight(wallet)
        
        k += 1
        if k > 25: # Takes longer than 5 seconds to start simplewallet
            error = utils.ErrorMessage("Error connecting simplewallet.")
            return error, 1
        
        time.sleep(0.2)
    
    dt = time.time() - start
    message = 'Wallet started successfully in ' + str(dt) + ' seconds'
    return message, 0

def walletJSONrpc(wallet, rpc_input):
    ''' walletJSONrpc() :: Send wallet JSON_RPC method and process initial result. '''
    
    # Add standard rpc values
    rpc_input.update(wallet.RPC_STANDARD_VALUES)
    
    # Execute the rpc request and return response output
    try:
        resp = req.post(wallet.RPC_URL,data=json.dumps(rpc_input),headers=wallet.RPC_STANDARD_HEADER)
        output = resp.json()
        
        # print(json.dumps(output, indent=2))
        
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

def makeTransferSplit(wallet, receive_addresses, amounts_atomic, payment_id, mixin):
    ''' makeTransferSplit() :: Make transaction(s), split up (Note: 1 Coin = 1e12 atomic units). '''
    
    # Prep destinations rpc array
    dests, err = _setupDestinations(receive_addresses, amounts_atomic)
    if err != 0:
        return dests, err
    
    # Create rpc data input
    params = { "destinations": dests, "mixin": mixin, "payment_id": payment_id, "new_algorithm": False }
    rpc_input = { "method": "transfer_split", "params": params }
    
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

def queryKey(wallet, key_type):
    ''' queryKey() :: Returns key info of type "key_type" ("mnemonic" or "view_key"). '''
    
    # Create rpc data input
    rpc_input = { "method": "query_key", "params": {"key_type": key_type} }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            return result["key"], 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'queryKey'.")
            return error, 1
    else:
        return result, err

def sweepDust(wallet):
    ''' sweepDust() :: Get all wallet inputs that are too small and sweep. '''
    
    # Create rpc data input
    rpc_input = { "method": "sweep_dust" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
        
    # Return formatted result
    if err == 0:
        try:
            return result["tx_hash_list"], 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'sweepDust'.")
            return error, 1
    else:
        return result, err

def stopWallet(wallet):
    ''' stopWallet() :: Cleanly disconnect simplewallet from daemon and exit. '''
    
    # Create rpc data input
    rpc_input = { "method": "stop_wallet" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            return result, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'stopWallet'.")
            return error, 1
    else:
        return result, err

def rescanBlockchain(wallet):
    ''' rescanBlockchain() :: Re-scan blockchain for wallet transactions from genesis. '''
    
    # Create rpc data input
    rpc_input = { "method": "rescan_blockchain" }
    
    # Get RPC result
    result, err = walletJSONrpc(wallet, rpc_input)
    
    # Return formatted result
    if err == 0:
        try:
            return result, 0
        except:
            error = utils.ErrorMessage("Error returning result fom 'rescanBlockchain'.")
            return error, 1
    else:
        return result, err
