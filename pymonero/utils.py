import os
import binascii

def gen_payment_id():
    # Generate 32 random bytes
    random_32_bytes = os.urandom(32)
    
    # Return as hex string
    random_hex = binascii.hexlify(random_32_bytes)
    payment_id = "".join(random_hex.decode("utf-8"))
    return payment_id

def atomic_to_coins(units):
    return units / 1000000000000.0
    
def coins_to_atomic(coins):
    return int(coins * 1000000000000)
    
class ErrorMessage:
    def __init__(self, error):
        self.error = error
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)