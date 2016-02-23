import pymonero
import sys

# Initialize daemon (optional unless using different parameters)
daemon = pymonero.connections.Daemon()
bitmonero = pymonero.Bitmonero(daemon)

# Get current bitmonerod information
try:
    get_info = bitmonero.get_info()
except:
    print('Error connecting to bitmonerod.')
    sys.exit()
print('\n\nBitmonerod Information:\n-----------------------')
print(get_info.to_JSON()) 


print('\n\nGeneral Information:\n--------------------')

# Get daemon connections information
get_connections = bitmonero.get_connections()
print('\nConnection Information:')
print(get_connections.to_JSON())


block_count = bitmonero.get_block_count()
print('\nTotal block count: ' + str(block_count))

hard_fork_info = bitmonero.hard_fork_info()
print('\nHard fork info:')
print(hard_fork_info.to_JSON())

# Get block header information for most recent block from height
last_block_header = bitmonero.get_last_block_header()
block_header = bitmonero.get_block_header_by_height(get_info.height-1)
print('\n\nBlock Header Information:\n-------------------------')
print(last_block_header.to_JSON())
print(block_header.to_JSON())

# Get block hash:
block_hash = bitmonero.get_block_hash(get_info.height-1)
print(block_hash)

# Get all block information for most recent block from hash
block_info = bitmonero.get_block_by_hash(block_header.hash)
print('\n\nBlock Information:\n------------------')
print(block_info.to_JSON())

# Get information on any transactions in block
n_txs = len(block_info.details.tx_hashes)
if n_txs > 0:
    print('\n\nTransactions:\n-------------')
    print('There are ' + str(n_txs) + ' non-coinbase transactions in block ' + str(block_info.header.height))
    transactions = bitmonero.get_transactions(block_info.details.tx_hashes, block_info.header.height)
    for i in range(0, n_txs):
        print(transactions[i].to_JSON())
else:
    print('There are no non-coinbase transactions in block ' + str(block_info.header.height))

# Get block template information
address = "44GBHzv6ZyQdJkjqZje6KLZ3xSyN1hBSFAnLP6EAqJtCRVzMzZmeXTC2AHKDS9aEDTRKmo6a6o9r9j86pYfhCWDkKjbtcns"
reserve_size = 200
block_template = bitmonero.get_block_template(address, reserve_size)
print('\n\nBlock Template:\n---------------')
print(block_template.to_JSON())

