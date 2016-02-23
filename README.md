# pymonero

A Monero daemon RPC connection tool in python. See `LICENSE` for use.

# Usage

See `test.py` for example script.

## Initialize daemon connection

pymonero requires `bitmonerod` to be running. If it is not running on localhost at the default port, you can configure a different setting.

Using the default host and port,

```python
bitmonero = pymonero.Bitmonero()
print(bitmonero.to_JSON())
```

If you want to change the default host and port,

```python
daemon = pymonero.connections.Daemon('http://127.0.0.1","18083")
bitmonero = pymonero.Bitmonero(daemon)
print(bitmonero.to_JSON())
```

### Get current bitmonerod information

```python
get_info = bitmonero.get_info()
print(get_info.to_JSON())
```
    
### Get daemon connections information

```python
get_connections = bitmonero.get_connections()
print(get_connections.to_JSON())
```

### Get block count

```python
block_count = bitmonero.get_block_count()
print('\nTotal block count: ' + str(block_count))
```

### Get hard fork info

```python
hard_fork_info = bitmonero.hard_fork_info()
print(hard_fork_info.to_JSON())
```

### Get block header information for most recent block from height

```python
last_block_header = bitmonero.get_last_block_header()
print(last_block_header.to_JSON())
```

### Get block header information for a specific height

```python
height = 900000
block_header = bitmonero.get_block_header_by_height(height)
print(block_header.to_JSON())
```

### Get block hash from height:

```python
height = 900000
block_hash = bitmonero.get_block_hash(height)
print(block_hash)
```

### Get all block information for most recent block from hash

```python
height = 900000
block_hash = bitmonero.get_block_hash(height)
block_info = bitmonero.get_block_by_hash(block_hash)
print(block_info.to_JSON())
```

### Get information on any transactions in block

```python
height = 900000
block_info = bitmonero.get_block_by_height(height)
n_txs = len(block_info.details.tx_hashes)
if n_txs > 0:
    print('There are ' + str(n_txs) + ' non-coinbase transactions in block ' + str(block_info.header.height))
    transactions = bitmonero.get_transactions(block_info.details.tx_hashes, block_info.header.height)
    for i in range(0, n_txs):
        print(transactions[i].to_JSON())
else:
    print('There are no non-coinbase transactions in block ' + str(block_info.header.height))
```

### Get block template information

```python
address = "44GBHzv6ZyQdJkjqZje6KLZ3xSyN1hBSFAnLP6EAqJtCRVzMzZmeXTC2AHKDS9aEDTRKmo6a6o9r9j86pYfhCWDkKjbtcns"
reserve_size = 200
block_template = bitmonero.get_block_template(address, reserve_size)
print(block_template.to_JSON())
```

# Acknowledgements

Some initial code inspired by [Monero Examples](https://moneroexamples.github.io/python-json-rpc/)
