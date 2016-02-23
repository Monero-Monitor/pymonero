from . import rpc as _rpc
from . import connections as _conns

class Bitmonero:
    def __init__(self, daemon=None):
        if daemon is not None and isinstance(daemon, _conns.Daemon):
            # if a valid connections.Daemon object is provided, use it
            self.daemon = daemon
        else:
            # if no valid connections.Daemon object is provided, use default
            self.daemon = _conns.Daemon()
    
    # Get current bitmonerod info
    def get_info(self):
        return _rpc.getDaemonInfo(self.daemon)
    
    # Get connections info
    def get_connections(self):
        return _rpc.getConnections(self.daemon)
    
    # Get block count
    def get_block_count(self):
        return _rpc.getBlockCount(self.daemon)
    
    # Get hard fork information
    def hard_fork_info(self):
        return _rpc.hardForkInfo(self.daemon)
        
    # Get block template
    def get_block_template(self, wallet_address, reserve_size):
        return _rpc.getBlockTemplate(self.daemon, wallet_address, reserve_size)
    
    # Get block hash
    def get_block_hash(self, block_height):
        return _rpc.getBlockHash(self.daemon, block_height)
    
    # Get last block header
    def get_last_block_header(self):
        return _rpc.getLastBlockHeader(self.daemon)
    
    # Get block header by block height
    def get_block_header_by_height(self, block_height):
        return _rpc.getBlockHeaderByHeight(self.daemon, block_height)
    
    # Get block header by block hash
    def get_block_header_by_hash(self, block_hash):
        return _rpc.getBlockHeaderByHash(self.daemon, block_hash)
    
    # Get block info by block height
    def get_block_by_height(self, block_height):
        return _rpc.getBlockByHeight(self.daemon, block_height)
    
    # Get block info by block hash
    def get_block_by_hash(self, block_hash):
        return _rpc.getBlockByHash(self.daemon, block_hash)
    
    # Get transaction info by tx hash
    def get_transactions(self, tx_hash, block=None):
        return _rpc.getTransactions(self.daemon, tx_hash, block)
