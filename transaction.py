class Transaction:
    
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        
    def __repr__(self):
        return (
            f"{self.sender} -> "
            f"{self.receiver}: "
            f"{self.amount}"
        )