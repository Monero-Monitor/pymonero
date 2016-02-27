import pymonero
import sys

# Initialize 2 simple wallets, one not connected, and one connected
user_host = 'http://localhost'
user_port = ['18083', '18082']
walletID = []
simplewallet = []
for i in range(0, len(user_port)):
    walletID.append(pymonero.connections.Wallet(user_host, user_port[i]))
    simplewallet.append(pymonero.SimpleWallet(walletID[i]))

# Test wallet functions:
for i in range(0, len(user_port)):
    
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
    print('\n\nSimple Wallet Height:\n----------------------')
    print('Simple wallet at port ' + user_port[i])
    wallet_height, err = simplewallet[i].get_height()
    if err == 0:
        print(wallet_height)
    else:
        print(wallet_height.error)
    
    # Make Simple Wallet Transfer:
    print('\n\nSimple Wallet Transfer:\n----------------------')
    print('Simple wallet at port ' + user_port[i])
    receive_address = '49VtwYXDbbh7hq57wwkLH36x4D6XV6Tr2P93ANnBi9qFGyYZbx8SXWPUHC9V1o7N41b4c3WJ1kubkffRfPTPfMuB8QUqFD5'
    amount_atomic = 1000000000000
    mixin = 3
    payment_id = pymonero.utils.gen_payment_id()
    transfer_result, err = simplewallet[i].make_transfer(receive_address, amount_atomic, payment_id, mixin)
    if err == 0:
        print(transfer_result.to_JSON())
    else:
        print(transfer_result.error)
