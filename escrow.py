import time,json,os,subprocess,requests
from iota import Iota, ProposedTransaction, Address, TryteString, Fragment, Transaction,adapter,ProposedBundle
from iota.crypto.addresses import AddressGenerator

class Escrow:
    def __init__(self,node='https://nodes.thetangle.org:443'):
        self.seed = self.getSeed()
        self.api = Iota(node,self.seed)

    #Generates a seed to act as the escrow
    def getSeed(self):
        if not os.path.isfile('seed.txt'):
            subprocess.run(['./generateSeed'])
            print("Placed new seed in seed.txt")
        return open('seed.txt').read().strip().encode('utf-8')
    
    #Creates an escrow process
    def create(self,collateral,fee=0,deposit=None):
        self.fee=0
        if self.requestDeposit(collateral,deposit):
            while not self.checkCondition():
                sleep(3)
        self.finalizeEscrow()
                
    
    def requestDeposit(self,collateral,deposit=None):
        if deposit is None:
            self.deposit = input("What is the deposit address: ")
        self.holdingAddress = self.api.get_new_addresses(count=None,checksum=True)['addresses'][0]
        print(f"You have 1 min to deposit {collateral} MIOTA to {self.holdingAddress}")
        count = 0
        while count < 60:
            time.sleep(1)
            balance = self.getBalance(self.holdingAddress)
            if balance >= collateral:
                print("Successfully deposited into escrow",balance)
                return True
        return False


    def checkCondition(self):
        #Go to ledger and check for condition.
        #Use streams?
        return True

    def finalizeEscrow(self):
        #Return money to deposit address
        returnAmount=self.getBalance(self.holdingAddress)
        if returnAmount > 0:
            returnAmount -= self.fee
            
        message="Repayment testing."
        feeLocation = self.api.get_new_addresses(count=1,checksum=True)['addresses'][0]
        txs = [
            ProposedTransaction(
                address = Address(self.deposit),
                value = returnAmount,
                message = TryteString.from_unicode(message)
            ),
        ]
        inputs = [Address(self.holdingAddress),]
        bundle = self.api.send_transfer(transfers=txs)['bundle']
        print(bundle.transactions[0].hash)
        print("Sent money back to recipient")
        self.addRevenue(fee)

    def getBalance(self,address):
        try:
            response = self.api.get_balances(addresses=[address])['balances']
            return response[0]
        except requests.exceptions.ConnectionError as e:
            print("Error contacting server; retrying")
            return getBalance(self,address)
        
    def addRevenue(self,money,filename='profits.txt'):
        if not os.path.isfile(filename):
            open('profits.txt','w+').write('0')
        current = int(open(filename).read().strip())
        current+=money
        open(filename).write(current)
    def getRevenue(self,filename="profits.txt"):
        if not os.path.isfile(filename): return 0
        return int(open(filename).read().strip())
    
    def sendRevenue(self,outputAddress):
        revenue = self.getRevenue()
        message="Output fees from escrow."
        txs = [
            ProposedTransaction(
                address = Address(outputAddress),
                value = revenue,
                message = TryteString.from_unicode(message)
            ),
        ]
        bundle = self.api.send_transfer(transfers=txs)['bundle']
        print(bundle.transactions[0].hash)

def createEscrow(args):
    escrow = Escrow()
    escrow.create(50,7,node=args.node)
    
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Basic escrow using IOTA.')
    parser.add_argument('collateral', type=int, help='The collateral costs.')
    parser.add_argument('fee', type=int, help='Non-refundable costs.')
    parser.add_argument('--seed', type=str, help='The seed to use, does not save.')
    parser.add_argument('--node', type=str, help='The iota node to use.',default='https://nodes.thetangle.org:443')
    parser.set_defaults(func=createEscrow)
    args = parser.parse_args()
    args.func(args)
