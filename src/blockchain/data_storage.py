"""
Blockchain Data Storage Module
Handles decentralized storage of experimental data and results.
"""

from typing import Dict, Optional, List
from datetime import datetime
from dataclasses import dataclass
import json
import hashlib
import time
from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

@dataclass
class DataBlock:
    """Represents a block of experimental data"""
    block_id: str
    timestamp: datetime
    data: Dict
    previous_hash: Optional[str]
    hash: str
    nonce: int = 0

class BlockchainStorage:
    """Main class for blockchain-based data storage"""
    
    def __init__(self):
        self.chain: List[DataBlock] = []
        self.pending_data: List[Dict] = []
        self.difficulty = 4  # Number of leading zeros required in hash
        
        # Initialize Web3 connection
        load_dotenv()
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_NODE_URL', 'http://localhost:8545')))
        
        # Load contract ABI and address
        with open('contracts/DataStorage.json', 'r') as f:
            contract_data = json.load(f)
            self.contract_abi = contract_data['abi']
            self.contract_address = contract_data['address']
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
    
    def _calculate_hash(self, block: DataBlock) -> str:
        """Calculate the hash of a block"""
        block_string = json.dumps({
            'block_id': block.block_id,
            'timestamp': block.timestamp.isoformat(),
            'data': block.data,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _mine_block(self, block: DataBlock) -> DataBlock:
        """Mine a block by finding a valid nonce"""
        while True:
            block.nonce += 1
            block.hash = self._calculate_hash(block)
            if block.hash.startswith('0' * self.difficulty):
                return block
    
    def add_data(self, data: Dict) -> str:
        """Add new data to the pending transactions"""
        self.pending_data.append({
            "timestamp": datetime.now(),
            "data": data
        })
        return "pending"
    
    def create_block(self, data: Dict) -> DataBlock:
        """Create a new block with the given data"""
        previous_block = self.chain[-1] if self.chain else None
        previous_hash = previous_block.hash if previous_block else None
        
        block = DataBlock(
            block_id=f"block_{len(self.chain)}",
            timestamp=datetime.now(),
            data=data,
            previous_hash=previous_hash,
            hash="",
            nonce=0
        )
        
        # Mine the block
        block = self._mine_block(block)
        
        # Store on Ethereum blockchain
        self._store_on_ethereum(block)
        
        self.chain.append(block)
        return block
    
    def _store_on_ethereum(self, block: DataBlock) -> None:
        """Store block data on Ethereum blockchain"""
        try:
            # Prepare transaction
            account = Account.from_key(os.getenv('ETH_PRIVATE_KEY'))
            nonce = self.w3.eth.get_transaction_count(account.address)
            
            # Convert block data to bytes
            block_data = json.dumps({
                'block_id': block.block_id,
                'timestamp': block.timestamp.isoformat(),
                'data': block.data,
                'previous_hash': block.previous_hash,
                'hash': block.hash,
                'nonce': block.nonce
            }).encode()
            
            # Create transaction
            transaction = self.contract.functions.storeData(
                block.block_id,
                block_data
            ).build_transaction({
                'chainId': int(os.getenv('ETH_CHAIN_ID', '1')),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, account.key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
        except Exception as e:
            print(f"Failed to store data on Ethereum: {str(e)}")
            # Continue with local storage even if blockchain storage fails
    
    def get_block(self, block_id: str) -> Optional[DataBlock]:
        """Retrieve a block by its ID"""
        # First try to get from local chain
        local_block = next((block for block in self.chain if block.block_id == block_id), None)
        if local_block:
            return local_block
        
        # If not found locally, try to get from blockchain
        try:
            block_data = self.contract.functions.getData(block_id).call()
            if block_data:
                block_dict = json.loads(block_data.decode())
                return DataBlock(
                    block_id=block_dict['block_id'],
                    timestamp=datetime.fromisoformat(block_dict['timestamp']),
                    data=block_dict['data'],
                    previous_hash=block_dict['previous_hash'],
                    hash=block_dict['hash'],
                    nonce=block_dict['nonce']
                )
        except Exception as e:
            print(f"Failed to retrieve block from blockchain: {str(e)}")
        
        return None
    
    def verify_chain(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Verify hash
            if current_block.previous_hash != previous_block.hash:
                return False
            
            # Verify block hash
            if current_block.hash != self._calculate_hash(current_block):
                return False
            
            # Verify proof of work
            if not current_block.hash.startswith('0' * self.difficulty):
                return False
        
        return True
    
    def get_chain_summary(self) -> Dict:
        """Get a summary of the blockchain"""
        return {
            "total_blocks": len(self.chain),
            "pending_transactions": len(self.pending_data),
            "is_valid": self.verify_chain(),
            "last_block_hash": self.chain[-1].hash if self.chain else None,
            "difficulty": self.difficulty
        } 