import hashlib
import json
import time

from transaction import Transaction


class Block:
    def __init__(self, index: int, transactions: list[Transaction], previous_hash: str):
        self.timestamp = time.time()            # 块的时间戳
        
        self.index = index                      # 块的索引
        self.transactions = transactions        # 块的交易数据（交易的list）
        self.previous_hash = previous_hash      # 上一个块的哈希值（string 类型）
        
        self.hash = self.calculate_hash()       # 本块的哈希值
        
    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": str(self.transactions),
            "previous_hash": self.previous_hash
        }
        
        block_string = json.dumps(block_data, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []
        self.pending_transactions: list[Transaction] = []
        
        self.create_genesis_block()
    
    def create_genesis_block(self):
        '''创建创世区块'''
        genesis_block = Block(
            index=0, 
            data="Genesis Block",
            previous_hash='0'
        )
        
        self.chain.append(genesis_block)
        
    def add_block(self, data):
        prev_block: Block = self.chain[-1]
        
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=prev_block.hash
            )

        self.chain.append(new_block)
        
    def is_valid(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]
            
            # 检查区块没有被修改
            if curr_block.hash != curr_block.calculate_hash():
                return False
            
            # 检查区块指向正确的上个区块
            if curr_block.previous_hash != prev_block.hash:
                return False
            
        return True
        
    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        
    def create_block(self):
        '''模拟挖矿'''
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.chain[-1].hash
        )
        
        self.chain.append(block)
        self.pending_transactions = []
        
    def get_balance(self, address):
        balance = 0
        
        for block in self.chain:
            
            for tx in block.transactions:
                
                if tx.sender == address:
                    balance -= tx.amount
                
                if tx.receiver == address:
                    balance += tx.amount
        
        return balance