import pymonero
import sys

# Initialize daemon (optional unless using different parameters)
daemon = pymonero.connections.Daemon()
bitmonero = pymonero.Bitmonero(daemon)


print('\n\nBitmonerod Information:\n-----------------------')

get_info = bitmonero.get_info()
if hasattr(get_info,"error"):
    print(get_info.error)
    sys.exit() # Since this is the first check, exit on error (likely bitmonerod unavailable)
else:
    print(get_info.to_JSON())


print('\n\nGeneral Information:\n--------------------')

print('\nConnection Information:')

get_connections = bitmonero.get_connections()
if hasattr(get_connections,"error"):
    print(get_connections.error)
else:
    print(get_connections.to_JSON())


print('\nHard fork info:')

hard_fork_info = bitmonero.hard_fork_info()
if hasattr(hard_fork_info,"error"):
    print(hard_fork_info.error)
else:
    print(hard_fork_info.to_JSON())


print('\nTotal block count:')

block_count = bitmonero.get_block_count()
if hasattr(block_count,"error"):
    print(block_count.error)
else:
    print(block_count)


print('\n\nBlock Header Information:\n-------------------------')

print('\nMost recent block:')

last_block_header = bitmonero.get_last_block_header()
if hasattr(last_block_header,"error"):
    print(last_block_header.error)
else:
    print(last_block_header.to_JSON())


print('\nBlock height 980274:')

block_header = bitmonero.get_block_header_by_height(980274)
if hasattr(block_header,"error"):
    print(block_header.error)
else:
    print(block_header.to_JSON())


print('\nBlock height 2000000:')

block_header = bitmonero.get_block_header_by_height(2000000)
if hasattr(block_header,"error"):
    print(block_header.error)
else:
    print(block_header.to_JSON())


print('\n\nBlock Information:\n------------------')

print('\nBlock hash for height 912345:')

block_hash = bitmonero.get_block_hash(912345)
if hasattr(block_hash,"error"):
    print(block_hash.error)
else:
    print(block_hash)


print('\nBlock info for hash from block 912345:')

block_info = bitmonero.get_block_by_hash(block_hash)
if hasattr(block_info,"error"):
    print(block_info.error)
else:
    print(block_info.to_JSON())


print('\n\nTransactions:\n-------------')

print('\nCheck two valid txs:')

transactions = bitmonero.get_transactions(["d6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if hasattr(transactions,"error"):
    print(transactions.error)
else:
    print(transactions.to_JSON())


print('\nCheck one valid and one invalid txs:')

transactions = bitmonero.get_transactions(["a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if hasattr(transactions,"error"):
    print(transactions.error)
else:
    print(transactions.to_JSON())


print('\nCheck two invalid txs:')

transactions = bitmonero.get_transactions(["a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408","ac3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"])
if hasattr(transactions,"error"):
    print(transactions.error)
else:
    print(transactions.to_JSON())


print('\n\nBlock Template:\n---------------')

address = "44GBHzv6ZyQdJkjqZje6KLZ3xSyN1hBSFAnLP6EAqJtCRVzMzZmeXTC2AHKDS9aEDTRKmo6a6o9r9j86pYfhCWDkKjbtcns"
reserve_size = 200
block_template = bitmonero.get_block_template(address, reserve_size)
if hasattr(block_template,"error"):
    print(block_template.error)
else:
    print(block_template.to_JSON())
