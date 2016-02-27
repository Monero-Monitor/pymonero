import json

class WalletBalance:
    ''' WalletBalance :: Class used to parse simplewallet info from "getbalance" rpc call. '''
    
    def __init__(self, result):
        self.balance          = result["balance"]
        self.unlocked_balance = result["unlocked_balance"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

class Payment:
    ''' Payment :: Class used to parse simplewallet info from "get_payments" rpc call. '''
    def __init__(self,payments):
        self.tx_hash      = payments["tx_hash"]
        self.amount       = payments["amount"]
        self.block_height = payments["tx_hash"]
        self.payment_id   = payments["block_height"]
        self.unlock_time  = payments["unlock_time"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)

class TransferResult:
    ''' TransferResult :: Class used to parse results from simplewallet "transfer" rpc call. '''
    
    def __init__(self, result):
        self.tx_key  = result["tx_key"]
        self.tx_hash = result["tx_key"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
