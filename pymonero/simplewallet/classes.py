import json

# WalletBalance :: Class used to parse simplewallet info from "getbalance" rpc call
class WalletBalance:
    def __init__(self, result):
        if not "balance" in result:
            errormsg = "getWalletBalance, WalletBalance: 'balance' not found in result."
            print(errormsg)
            raise RuntimeError(errormsg)
            return
        if not "unlocked_balance" in result:
            errormsg = "getWalletBalance, WalletBalance: 'unlocked_balance' not found in result."
            print(errormsg)
            raise RuntimeError(errormsg)
            return
        self.balance          = result["balance"]
        self.unlocked_balance = result["unlocked_balance"]
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)