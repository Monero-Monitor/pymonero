import pymonero
import sys

# Initialize daemon (optional unless using different parameters)
daemon = pymonero.connections.Daemon()
bitmonero = pymonero.Bitmonero(daemon)


# Get current bitmonerod information
print('\n\nBitmonerod Information:\n-----------------------')
get_info, err = bitmonero.get_info()
if err == 0:
    print(get_info.to_JSON())
else:
    print(get_info.error)
    sys.exit() # Since this is the first check, exit on error (likely bitmonerod unavailable)

print('\n\nGeneral Information:\n--------------------')

# Get daemon connections information
print('\nConnection Information:')
get_connections, err = bitmonero.get_connections()
if err == 0:
    print(get_connections.to_JSON())
else:
    print(get_connections.error)

# Get hard fork information
print('\nHard fork info:')
hard_fork_info, err = bitmonero.hard_fork_info()
if err == 0:
    print(hard_fork_info.to_JSON())
else:
    print(hard_fork_info.error)

# Get block count
print('\nTotal block count:')
block_count, err = bitmonero.get_block_count()
if err == 0:
    print(block_count)
else:
    print(block_count.error)


# Get block header information for most recent block from height
print('\n\nBlock Header Information:\n-------------------------')
last_block_header, err = bitmonero.get_last_block_header()
if err == 0:
    print(last_block_header.to_JSON())
else:
    print(last_block_header.error)

block_header, err = bitmonero.get_block_header_by_height(980274)
if err == 0:
    print(block_header.to_JSON())
else:
    print(block_header.error)

# Look up too high of a block height:
block_header, err = bitmonero.get_block_header_by_height(2000000)
if err == 0:
    print(block_header.to_JSON())
else:
    print(block_header.error)

# Get all block information for most recent block from hash
print('\n\nBlock Information:\n------------------')
block_hash, err = bitmonero.get_block_hash(912345)
if err == 0:
    print(block_hash)
else:
    print(block_hash.error)

block_info, err = bitmonero.get_block_by_hash(block_hash)
if err == 0:
    print(block_info.to_JSON())
else:
    print(block_info.error)

# Get information on transactions
print('\n\nTransactions:\n-------------')

# check good txs:
txs, err = bitmonero.get_transactions(["d6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if err == 0:
    for i in range(0,len(txs)):
        print(txs[i].to_JSON())
        print('\n\n')
else:
    print(txs.error)
    if hasattr(txs, 'missed_tx'):
        print(txs.missed_tx)

# check one good tx, one bad tx
txs, err = bitmonero.get_transactions(["a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if err == 0:
    for i in range(0,len(txs)):
        print(txs[i].to_JSON())
        print('\n\n')
else:
    print(txs.error)
    if hasattr(txs, 'missed_tx'):
        print(txs.missed_tx)
        
# check all bad txs:
txs, err = bitmonero.get_transactions(["a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","ac3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if err == 0:
    for i in range(0,len(txs)):
        print(txs[i].to_JSON())
        print('\n\n')
else:
    print(txs.error)
    if hasattr(txs, 'missed_tx'):
        print(txs.missed_tx)

# Get block template information
print('\n\nBlock Template:\n---------------')
address = "44GBHzv6ZyQdJkjqZje6KLZ3xSyN1hBSFAnLP6EAqJtCRVzMzZmeXTC2AHKDS9aEDTRKmo6a6o9r9j86pYfhCWDkKjbtcns"
reserve_size = 200
block_template, err = bitmonero.get_block_template(address, reserve_size)
if err == 0:
    print(block_template.to_JSON())
else:
    print(block_template.error)
