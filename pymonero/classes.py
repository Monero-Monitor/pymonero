import json

# DaemonInfo :: Class used to parse daemon info from "get_info" rpc call
class DaemonInfo:
    def __init__(self, result):
        self.status                     = result["status"]
        self.target                     = result["target"]
        self.grey_peerlist_size         = result["grey_peerlist_size"]
        self.incoming_connections_count = result["incoming_connections_count"]
        self.white_peerlist_size        = result["white_peerlist_size"]
        self.alt_blocks_count           = result["alt_blocks_count"]
        self.outgoing_connections_count = result["outgoing_connections_count"]
        self.height                     = result["height"]
        self.difficulty                 = result["difficulty"]
        self.testnet                    = result["testnet"]
        self.target_height              = result["target_height"]
        self.tx_pool_size               = result["tx_pool_size"]
        self.top_block_hash             = result["top_block_hash"]
        self.tx_count                   = result["tx_count"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Connections :: Class used to parse details from "get_connections" json_rpc method
class Connections:
    def __init__(self, result):
        self.status = result["status"]
        self.connections = []
        for i in range(0, len(result["connections"])):
            self.connections.append(result["connections"][i])
            
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Connection :: Used to parse single connection, ex: in class "Connections"
class Connection:
    def __init__(self, conn):
        self.current_download = conn["current_download"]
        self.incoming         = conn["incoming"]
        self.local_ip         = conn["local_ip"]
        self.ip               = conn["ip"]
        self.recv_count       = conn["recv_count"]
        self.send_count       = conn["send_count"]
        self.avg_upload       = conn["avg_upload"]
        self.avg_download     = conn["avg_download"]
        self.peer_id          = conn["peer_id"]
        self.live_time        = conn["live_time"]
        self.port             = conn["port"]
        self.current_upload   = conn["current_upload"]
        self.state            = conn["state"]
        self.send_idle_time   = conn["send_idle_time"]
        self.recv_idle_time   = conn["recv_idle_time"]
        self.localhost        = conn["localhost"]
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# BlockInfo :: Class used to parse block header and details from "getblock" rpc call
class BlockInfo:
    def __init__(self, header, info):
        self.header = BlockHeader(header)
        self.details = BlockDetails(info)
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# BlockHeader :: Class used to parse block header, ex: in class "BlockInfo"
class BlockHeader:
    def __init__(self, header):
        self.nonce         = header["nonce"]
        self.reward        = header["reward"]
        self.hash          = header["hash"]
        self.timestamp     = header["timestamp"]
        self.major_version = header["major_version"]
        self.minor_version = header["minor_version"]
        self.difficulty    = header["difficulty"]
        self.depth         = header["depth"]
        self.prev_hash     = header["prev_hash"]
        self.orphan_status = header["orphan_status"]
        self.height        = header["height"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# BlockDetails :: Class used to parse block details, ex: in class "BlockInfo"
class BlockDetails:
    def __init__(self, info):
        self.nonce         = info["nonce"]
        self.timestamp     = info["timestamp"]
        self.tx_hashes     = info["tx_hashes"]
        self.major_version = info["major_version"]
        self.prev_id       = info["prev_id"]
        self.minor_version = info["minor_version"]
        self.miner_tx      = MinerTx(info["miner_tx"])
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# MinerTx  :: Class used to parse "miner_tx" info, ex: in class "BlockInfo"
class MinerTx:
    def __init__(self, miner_tx_info): 
        self.signatures  = miner_tx_info["signatures"]
        self.extra       = miner_tx_info["extra"]
        self.unlock_time = miner_tx_info["unlock_time"]
        self.vin         = []
        for i in range(0,len(miner_tx_info["vin"])):
            self.vin.append(Vin(miner_tx_info["vin"][i]))
        self.vout        = []
        for i in range(0,len(miner_tx_info["vout"])):
            self.vout.append(Vout(miner_tx_info["vout"][i]))
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Vout :: Class used to parse tx "vout", ex: in class "MinerTx"
class Vout:
    def __init__(self, vout_miner_tx):
        self.amount = vout_miner_tx["amount"]
        self.target = VoutTarget(vout_miner_tx["target"])
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# VoutTarget :: Class used to parse vout "target", ex: in class "Vout"
class VoutTarget:
    def __init__(self, target_vout):
        self.key = target_vout["key"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Vin :: Class used to parse tx "vin", ex: in class "MinerTx"
class Vin:
    def __init__(self, vin):
        if "gen" in vin:
            self.gen = VinGen(vin["gen"])
        if "key" in vin:
            self.key = VinKey(vin["key"])
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# VinGen :: Class used to parse vin "gen", ex: in class "Vin"
class VinGen:
    def __init__(self, gen):
        self.height = gen["height"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# VinKey :: Class used to parse vin "gen", ex: in class "Vin"
class VinKey:
    def __init__(self, key):
        self.amount = key["amount"]
        self.k_image = key["k_image"]
        self.key_offsets = key["key_offsets"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Transactions :: Class used to parse txs from "/gettransactions" method
class Transactions:
    def __init__(self, hashes, txs_as_json, block=None):
        n_txs = len(txs_as_json)
        self.txs = []
        for i in range(0,n_txs):
            output_json_str = str(txs_as_json[i])
            output_json_str.replace('\\', '')
            output_json = json.loads(output_json_str)
            self.txs.append(Transaction(hashes[i], output_json))
        if block is not None:
            self.block = block
            
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# Transaction :: Class used to parse individual transactions, ex: in class "Transactions"
class Transaction:
    def __init__(self, hash, tx_info, block=None):
        self.hash        = hash
        self.version     = tx_info["version"]
        self.signatures  = tx_info["signatures"]
        self.extra       = tx_info["extra"]
        self.unlock_time = tx_info["unlock_time"]
        self.vin         = []
        for i in range(0,len(tx_info["vin"])):
            self.vin.append(Vin(tx_info["vin"][i]))
        self.vout        = []
        for i in range(0,len(tx_info["vout"])):
            self.vout.append(Vout(tx_info["vout"][i]))
        if block is not None:
            self.block = block
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

# BlockTemplate :: Class used to parse result from json_rpc "getblocktemplate" method
class BlockTemplate:
    def __init__(self,result):
        self.prev_hash          = result["prev_hash"]
        self.difficulty         = result["difficulty"]
        self.height             = result["height"]
        self.blocktemplate_blob = result["blocktemplate_blob"]
        self.reserved_offset    = result["reserved_offset"]
        self.status             = result["status"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

class HardForkInfo:
    def __init__(self,result):
        self.version         = result["version"]
        self.threshold       = result["threshold"]
        self.enabled         = result["enabled"]
        self.window          = result["window"]
        self.state           = result["state"]
        self.votes           = result["votes"]
        self.earliest_height = result["earliest_height"]
        self.voting          = result["voting"]
        self.status          = result["status"]
    
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
