import pymonero
import sys

# Initialize 2 simple wallets, one not connected, and one connected
user_host = 'http://127.0.0.1'
user_port = ['18082']
wallet_file = ["/absolute/path/to/wallet_file"]
wallet_pass = ["wallet_password"]
walletID = []
simplewallet = []
for i in range(0, len(user_port)):
    walletID.append(pymonero.connections.Wallet(user_host, user_port[i]))
    simplewallet.append(pymonero.SimpleWallet(walletID[i]))

# Test wallet functions:
for i in range(0, len(user_port)):
    
    # Stop wallet if currently running
    stop_wallet, err = simplewallet[i].stop_wallet()
    
    # Start wallet:
    message, err = simplewallet[i].start_wallet(wallet_file[i], wallet_pass[i])
    if err == 0:
        print(message)
    else:
        print(message.error)
    
    # Rescan Blockchain:
    print('\n\nSimple Wallet Rescan:\n---------------------')
    print('Simple wallet at port ' + user_port[i])
    rescan_blockchain, err = simplewallet[i].rescan_blockchain()
    if err != 0:
        print(rescan_blockchain.error)
    
    # Print Wallet Balance:
    print('\n\nSimple Wallet Balance:\n----------------------')
    print('Simple wallet at port ' + user_port[i])
    wallet_balance, err = simplewallet[i].get_balance()
    if err == 0:
        print(wallet_balance.to_JSON())
    else:
        print(wallet_balance.error)
    
    # Print Wallet Address:
    print('\n\nSimple Wallet Address:\n----------------------')
    print('Simple wallet at port ' + user_port[i])
    wallet_address, err = simplewallet[i].get_address()
    if err == 0:
        print(wallet_address)
    else:
        print(wallet_address.error)
    
    # Print Simple Wallet Height:
    print('\n\nSimple Wallet Height:\n---------------------')
    print('Simple wallet at port ' + user_port[i])
    wallet_height, err = simplewallet[i].get_height()
    if err == 0:
        print(wallet_height)
    else:
        print(wallet_height.error)
    
    # Print Wallet View Key:
    print('\n\nSimple Wallet View Key:\n-----------------------')
    print('Simple wallet at port ' + user_port[i])
    view_key, err = simplewallet[i].query_key("view_key")
    if err == 0:
        print(view_key)
    else:
        print(view_key.error)
    
    # Print Wallet Mnemonic:
    print('\n\nSimple Wallet Mnemonic:\n-----------------------')
    print('Simple wallet at port ' + user_port[i])
    mnemonic, err = simplewallet[i].query_key("mnemonic")
    if err == 0:
        print(mnemonic)
    else:
        print(mnemonic.error)
    
    # Make Simple Wallet Transfer:
    print('\n\nSimple Wallet Transfer:\n-----------------------')
    print('Simple wallet at port ' + user_port[i])
    receive_address = ['49VtwYXDbbh7hq57wwkLH36x4D6XV6Tr2P93ANnBi9qFGyYZbx8SXWPUHC9V1o7N41b4c3WJ1kubkffRfPTPfMuB8QUqFD5',
                       '48daf1rG3hE1Txapcsxh6WXNe9MLNKtu7W7tKTivtSoVLHErYzvdcpea2nSTgGkz66RFP4GKVAsTV14v6G3oddBTHfxP6tU']
    amount_atomic = [1500000000000, 1000000000000]
    mixin = 3
    payment_id = pymonero.utils.gen_payment_id()
    transfer_result, err = simplewallet[i].make_transfer(receive_address, amount_atomic, payment_id, mixin)
    if err == 0:
        print(transfer_result.to_JSON())
    else:
        print(transfer_result.error)
    
    # Print Wallet Sweep Dust:
    print('\n\nSimple Wallet Sweep Dust:\n-------------------------')
    print('Simple wallet at port ' + user_port[i])
    sweep_dust, err = simplewallet[i].sweep_dust()
    if err == 0:
        print(sweep_dust)
    else:
        print(sweep_dust.error)
    
    # Stop Simple Wallet:
    print('\n\nStop Simple Wallet:\n-------------------')
    print('Simple wallet at port ' + user_port[i])
    stop_wallet, err = simplewallet[i].stop_wallet()
    if err != 0:
        print(stop_wallet.error)
    
    
