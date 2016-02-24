import pymonero
import sys

# Initialize 2 simple wallets, one not connected, and one connected
user_host = 'http://localhost'
user_port = ['18083', '18082']
walletID = []
simplewallet = []
for i in range(0,len(userport)):
    walletID.append(pymonero.connections.Wallet(user_host, user_port[i]))
    simplewallet.append(pymonero.SimpleWallet(walletID[i]))

# Get wallet balances
for i in range(0,2):

    print('\n\nSimple Wallet Balance:\n----------------------')
    print('Simple wallet at port ' + user_port[i])
    try:
        wallet_balance = simplewallet[i].get_balance()
        print(wallet_balance.to_JSON())
    except:
        print('Error connecting to simple wallet.')

