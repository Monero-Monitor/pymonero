import sys
sys.path.append('../')
import json
import unittest
import pymonero
from pymonero.bitmonerod import classes
import testdata

class TestBitmoneroRPC(unittest.TestCase):
    
    def setUp(self):
        '''Necessary things before testing.'''
        
        self.bitmonero = pymonero.Bitmonero()
        
        # These unit tests require that a local instance of bitmonerod is running. Make sure!
        info = self.bitmonero.get_info()
            
        if hasattr(info,"error"):
            print('Error connecting to bitmonerod.')
            print(info.error)
            sys.exit()
            
    def test_get_info(self):
        '''Test that get_info() returns information as DaemonInfo class.'''
        
        def T(info):
            self.assertEqual(info.__class__, classes.DaemonInfo)
        
        info = self.bitmonero.get_info()
        T(info)
    
    def test_get_connections(self):
        '''Test that get_connections() returns information as Connections class.'''
        
        def T(conns):
            self.assertEqual(conns.__class__, classes.Connections)
        
        connections = self.bitmonero.get_connections()
        T(connections)
    
    def test_get_block_count(self):
        '''Test that get_block_count() returns information as int.'''
        
        def T(count):
            self.assertEqual(count.__class__, int)
            self.assertTrue(count > 0)
        
        block_count = self.bitmonero.get_block_count()
        T(block_count)
    
    def test_hard_fork_info(self):
        '''Test that hard_fork_info() returns information as HardForkInfo class.'''
        
        def T(info):
            self.assertEqual(info.__class__, classes.HardForkInfo)
        
        hard_fork_info = self.bitmonero.hard_fork_info()
        T(hard_fork_info)
    
    def test_get_last_block_header(self):
        '''Test that get_last_block_header() returns information as BlockHeader class.'''
        
        def T(header):
            self.assertEqual(header.__class__, classes.BlockHeader)
        
        last_block_header = self.bitmonero.get_last_block_header()
        T(last_block_header)
    
    def test_get_block_header_by_height(self):
        '''Test that get_block_header_by_height(h) returns correct information.'''
        
        def T(header):
            self.assertEqual(header.__class__, classes.BlockHeader)
            
            block_912345_header = testdata.BLOCK_912345_HEADER
            
            self.assertTrue(header.depth >= block_912345_header.depth)
            self.assertEqual(header.difficulty, block_912345_header.difficulty)
            self.assertEqual(header.hash, block_912345_header.hash)
            self.assertEqual(header.height, block_912345_header.height)
            self.assertEqual(header.major_version, block_912345_header.major_version)
            self.assertEqual(header.minor_version, block_912345_header.minor_version)
            self.assertEqual(header.nonce, block_912345_header.nonce)
            self.assertEqual(header.orphan_status, block_912345_header.orphan_status)
            self.assertEqual(header.prev_hash, block_912345_header.prev_hash)
            self.assertEqual(header.reward, block_912345_header.reward)
            self.assertEqual(header.timestamp, block_912345_header.timestamp)
        
        block_header = self.bitmonero.get_block_header_by_height(912345)
        T(block_header)
    
    def test_get_block_header_by_hash(self):
        '''Test that get_block_header_by_hash(h) returns correct information.'''
        
        def T(header):
            self.assertEqual(header.__class__, classes.BlockHeader)
            
            block_912345_header = testdata.BLOCK_912345_HEADER
            
            self.assertTrue(header.depth >= block_912345_header.depth)
            self.assertEqual(header.difficulty, block_912345_header.difficulty)
            self.assertEqual(header.hash, block_912345_header.hash)
            self.assertEqual(header.height, block_912345_header.height)
            self.assertEqual(header.major_version, block_912345_header.major_version)
            self.assertEqual(header.minor_version, block_912345_header.minor_version)
            self.assertEqual(header.nonce, block_912345_header.nonce)
            self.assertEqual(header.orphan_status, block_912345_header.orphan_status)
            self.assertEqual(header.prev_hash, block_912345_header.prev_hash)
            self.assertEqual(header.reward, block_912345_header.reward)
            self.assertEqual(header.timestamp, block_912345_header.timestamp)
        
        # hash is for block 912345
        block_header = self.bitmonero.get_block_header_by_hash("e22cf75f39ae720e8b71b3d120a5ac03f0db50bba6379e2850975b4859190bc6")
        T(block_header)
    
    def test_get_block_hash(self):
        '''Test that test_get_block_hash() returns information as str.'''
        
        def T(hash):
            block_912345_header = testdata.BLOCK_912345_HEADER
            self.assertEqual(hash, block_912345_header.hash)
        
        block_hash = self.bitmonero.get_block_hash(912345)
        T(block_hash)
    
    def test_get_block_by_height(self):
        '''Test that test_get_block_by_height(h) returns correct information.'''
        
        def T(block):
            self.assertEqual(block.__class__, classes.BlockInfo)
            
            block_912345_header = testdata.BLOCK_912345_HEADER
            block_912345_details = testdata.BLOCK_912345.details
            
            header = block.header
            self.assertTrue(header.depth >= block_912345_header.depth)
            self.assertEqual(header.difficulty, block_912345_header.difficulty)
            self.assertEqual(header.hash, block_912345_header.hash)
            self.assertEqual(header.height, block_912345_header.height)
            self.assertEqual(header.major_version, block_912345_header.major_version)
            self.assertEqual(header.minor_version, block_912345_header.minor_version)
            self.assertEqual(header.nonce, block_912345_header.nonce)
            self.assertEqual(header.orphan_status, block_912345_header.orphan_status)
            self.assertEqual(header.prev_hash, block_912345_header.prev_hash)
            self.assertEqual(header.reward, block_912345_header.reward)
            self.assertEqual(header.timestamp, block_912345_header.timestamp)
            
            
            details = block.details
            # Not going to check every returned detail. If the following checks pass, the 
            # remaining info (vin, vout, etc) will pass too. Point is, it did the json_rpc
            # call correctly.
            self.assertEqual(details.miner_tx.extra, block_912345_details.miner_tx.extra)
            self.assertEqual(details.miner_tx.signatures, block_912345_details.miner_tx.signatures)
            self.assertEqual(details.miner_tx.unlock_time, block_912345_details.miner_tx.unlock_time)
            self.assertEqual(details.nonce, block_912345_details.nonce)
            self.assertEqual(details.prev_id, block_912345_details.prev_id)
            self.assertEqual(details.timestamp, block_912345_details.timestamp)
        
        block = self.bitmonero.get_block_by_height(912345)
        T(block)
    
    def test_get_block_by_hash(self):
        '''Test that get_block_by_hash(h) returns correct information. Same checks as 
           test_get_block_by_height but variation on rpc lookup call.'''
        
        def T(block):
            self.assertEqual(block.__class__, classes.BlockInfo)
            
            block_912345_header = testdata.BLOCK_912345_HEADER
            block_912345_details = testdata.BLOCK_912345.details
            
            header = block.header
            self.assertTrue(header.depth >= block_912345_header.depth)
            self.assertEqual(header.difficulty, block_912345_header.difficulty)
            self.assertEqual(header.hash, block_912345_header.hash)
            self.assertEqual(header.height, block_912345_header.height)
            self.assertEqual(header.major_version, block_912345_header.major_version)
            self.assertEqual(header.minor_version, block_912345_header.minor_version)
            self.assertEqual(header.nonce, block_912345_header.nonce)
            self.assertEqual(header.orphan_status, block_912345_header.orphan_status)
            self.assertEqual(header.prev_hash, block_912345_header.prev_hash)
            self.assertEqual(header.reward, block_912345_header.reward)
            self.assertEqual(header.timestamp, block_912345_header.timestamp)
            
            
            details = block.details
            # (See note in test_get_block_by_height regarding what's checked.)
            self.assertEqual(details.miner_tx.extra, block_912345_details.miner_tx.extra)
            self.assertEqual(details.miner_tx.signatures, block_912345_details.miner_tx.signatures)
            self.assertEqual(details.miner_tx.unlock_time, block_912345_details.miner_tx.unlock_time)
            self.assertEqual(details.nonce, block_912345_details.nonce)
            self.assertEqual(details.prev_id, block_912345_details.prev_id)
            self.assertEqual(details.timestamp, block_912345_details.timestamp)
            self.assertEqual(details.tx_hashes, block_912345_details.tx_hashes)
        
        # hash is for block 912345
        block = self.bitmonero.get_block_by_hash("e22cf75f39ae720e8b71b3d120a5ac03f0db50bba6379e2850975b4859190bc6")
        T(block)
    
    def test_get_transactions(self):
        '''Test that test_get_transactions() returns correct tx information.'''
        
        def T(transactions):
            txs = transactions.found
            for i in range(0,len(txs)):
                self.assertEqual(txs[i].hash, testdata.TX_RETURN[i].hash)
                self.assertEqual(txs[i].version, testdata.TX_RETURN[i].version)
                self.assertEqual(txs[i].signatures, testdata.TX_RETURN[i].signatures)
                self.assertEqual(txs[i].extra, testdata.TX_RETURN[i].extra)
                self.assertEqual(txs[i].unlock_time, testdata.TX_RETURN[i].unlock_time)
            self.assertEqual(len(transactions.missed), 0)
        
        txs_hashes = ["d6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408",
            "dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"]
        transactions = self.bitmonero.get_transactions(txs_hashes)
        T(transactions)
    
    def test_get_transactions_one_missed(self):
        '''Test that test_get_transactions() returns correct tx information (w/ one missed).'''
        
        def T(transactions):
            txs = transactions.found
            self.assertEqual(len(txs), 2)
            for i in range(0,len(txs)):
                self.assertEqual(txs[i].hash, testdata.TX_RETURN[i].hash)
                self.assertEqual(txs[i].version, testdata.TX_RETURN[i].version)
                self.assertEqual(txs[i].signatures, testdata.TX_RETURN[i].signatures)
                self.assertEqual(txs[i].extra, testdata.TX_RETURN[i].extra)
                self.assertEqual(txs[i].unlock_time, testdata.TX_RETURN[i].unlock_time)
            self.assertEqual(len(transactions.missed), 1)
            self.assertEqual(transactions.missed, ["a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408"])
        
        # First hash is bad, second is good
        txs_hashes = ["d6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408",
            "a6e48158472848e6687173a91ae6eebfa3e1d778e65252ee99d7515d63090408",
            "dc3947fda74980c24274767b583b4c22d24e9afd98ec2fea5a9e66dcd12ad543"]
        transactions = self.bitmonero.get_transactions(txs_hashes)
        T(transactions)
    
    def test_get_block_template(self):
        '''Test that get_block_template() returns correct template.'''
        
        def T(template):
            self.assertEqual(template.__class__, classes.BlockTemplate)
                   
        address = "44GBHzv6ZyQdJkjqZje6KLZ3xSyN1hBSFAnLP6EAqJtCRVzMzZmeXTC2AHKDS9aEDTRKmo6a6o9r9j86pYfhCWDkKjbtcns"
        reserve_size = 200
        block_template = self.bitmonero.get_block_template(address, reserve_size)
        T(block_template)
        

if __name__ == "__main__":
    unittest.main()#warnings='ignore')