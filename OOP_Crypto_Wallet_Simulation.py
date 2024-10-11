"""
#Author: Noah Vich

#Topic: Crypto Wallet

#Abstract class: Transact
#Class: Crypto
#Class: NFT
#Class: Wallet

"""

from abc import ABC, abstractmethod
from datetime import datetime, date
import requests
import json



class Crypto:
    """Crypto object to be passed or sent in wallet.
    """
    def __init__ (self, blockchain, amount, strike_price = 0) :
        """Initialization of crypto object

        Args:
            blockchain (str): blockchain of currency
            amount (int): amount of currency
            strike_price (int, optional): Price currency bought at. Defaults to 0.
        """
        self._amount = amount
        self._strike_price = strike_price
        self._blockchain = blockchain
        
    @property
    def amount (self) :
        return self._amount
    @amount.setter
    def amount (self, amount) :
        self._amount = amount
        
    @property
    def strike_price (self) :
        return self._strike_price
    @strike_price.setter
    def strike_price (self, strike_price) :
        self._strike_price = strike_price
        
    @property
    def blockchain (self) :
        return self._blockchain
    @blockchain.setter
    def blokchain (self, blockchain) :
        self._blockchain = blockchain
    



class NFT:
    """NFT object to be passed or sent in wallet.
    """
    def __init__ (self, title, blockchain, amount, price = 0) :
        """Initialization of NFT object

        Args:
            title (str): title of NFT
            blockchain (str): blockchain NFT on
            amount (int): amount of NFT
            price (int, optional): Price of NFT as amount currency. Defaults to 0.
        """
        self._title = title
        self._blockchain = blockchain
        self._amount = amount
        self._price = price
        
    @property
    def title (self) :
        return self._title
    
    @title.setter
    def title (self, title) :
        self._title = title
        
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def blockchain(self):
        return self._blockchain

    @blockchain.setter
    def blockchain(self, blockchain):
        self._blockchain = blockchain

        
        


class Transact (ABC) :
    """Abstract class with transaction methods.
    """
    def __init__ (self, address) :
        """Initializes transact object

        Args:
            address (str): address origin of transaction
        """
        self._address = address
        

    @abstractmethod
    #implemented in Wallet
    def recieve(self, from_address, item) : 
        pass
    
    @abstractmethod
    #implemented in Wallet
    def send(self, to_address, item) :
        pass
    
        
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address




class Wallet (Transact):
    """Wallet class that can send and recieve crypto. Other methods include finding out value of crypto, and printing assets.

    Args:
        Transact (Class): Abstract transact class with recieve and send methods
    """
    
    acceptable_crypto = ['btc', 'eth', 'usdt', 'bnb', 'xrp', 'sol', 'usdc', 'ada', 'avax', 'doge'] #crytopcurrencies the wallet supports
    
    def __init__ (self, address) :
        """Initializes wallet object

        Args:
            address (str): address of wallet
        """
        self._address = address
        
        self._crypto_list = list() #all crypto in wallet
        self._NFT_list = list() #all NFT in wallet
        self._transactions = list() #all transactions of wallet
        
        
    def recieve(self, from_address, obj) :
        """Recieve crypto or NFT method

        Args:
            from_address (str): address which crypo recieved from
            obj (object): object of either Crypto or NFT type

        Returns:
            str: error message if applicable
        """
        item = []
        
        #if recieveing same crypto that already exists, do not create new object, only add to amount
        if isinstance(obj, Crypto) :
            item.append(obj._blockchain)
            item.append(obj._amount)
            item.append(obj._strike_price)
        
            if obj._blockchain in Wallet.acceptable_crypto :
                
                #for first crypto to be added to wallet
                if len(self._crypto_list) == 0 :
                    recieved_crypto = Crypto(item[0], item[1], item[2])
                    print(f"Recieved: {item[1]} of {item[0]} from '{from_address}' at {item[2]} spot price\n")
                    self._crypto_list.append(recieved_crypto)
            
                else : 
                    for crypto in self._crypto_list :
                        if item[0] == crypto._blockchain :
                            old_amount = crypto._amount #used in calculation of strike price
                            crypto._amount += item[1]
                            crypto._strike_price = round(((item[1] * item[2]) + (crypto._strike_price * old_amount)) / crypto._amount, 5) #average price of asset bought
                            print(f"Recieved: {item[1]} of {crypto._blockchain} from '{from_address}' at {item[2]} spot price\n")
                        
                        else : #if crypto not already in wallet
                            recieved_crypto = Crypto(item[0], item[1], item[2])
                            print(f"Recieved: {item[1]} of {item[0]} from '{from_address}' at {item[2]} spot price\n")
                            self._crypto_list.append(recieved_crypto)

            else :
                return f'Wallet cannot accept {item[0]} transaction' #if crypto not supported by wallet
        
        #if recieveing same NFT that already exists, do not create new object, only add to amount
        elif isinstance(obj, NFT):
            item.append(obj._title)
            item.append(obj._blockchain)
            item.append(obj._amount)
            item.append(obj._price)
                      
            # For first NFT to be added to wallet        
            if not self._NFT_list:  #Check if the NFT list is empty
                received_NFT = NFT(item[0], item[1], item[2], item[3])
                print(f"Recieved: {item[2]} NFT '{item[0]}' on {item[1]} from '{from_address}' for {item[3]}{item[1]}\n")
                self._NFT_list.append(received_NFT)
            else:
                for nft in self._NFT_list: 
                    if item[0] == nft._title and item[1] == nft._blockchain: #if existing nft
                        nft._amount += item[2]
                        nft._price = round(((nft._price * (nft._amount - item[2])) + (item[2] * item[3])) / nft._amount, 5) #calculate average price bought at
                        print(f"Recieved: {item[2]} NFT '{nft._title}' on {nft._blockchain} from '{from_address}' for {nft._price} {nft._blockchain}\n")
                        break
                    
                    else: #if nft not in list already
                        received_NFT = NFT(item[0], item[1], item[2], item[3])
                        print(f"Recieved: {item[2]} NFT '{item[0]}' on {item[1]} from '{from_address}' for {item[3]} on {item[1]}\n")
                        self._NFT_list.append(received_NFT)
                    
        
        else:
            return ValueError
        
        #add transaction to transactions
        transaction_info = (from_address, item)  
        now = datetime.today().strftime('%Y-%m-%d - %H:%M:%S')
        self._transactions.append([transaction_info, now, 'r']) #r = receive
        
        
    def send(self, to_address, obj) :
        """Send crypto or NFT method

        Args:
            to_address (str): address to send item to
            obj (object): instance of either Crypto or NFT type
        """
        #find item in crypto or NFT
        #remove amount of item
        item = []
        
        if isinstance(obj, Crypto) :
            item.append(obj._blockchain)
            item.append(obj._amount)
            item.append(obj._strike_price)
            
            if item[0] in Wallet.acceptable_crypto : #if crypto
                for held_crypto in self._crypto_list :
                
                    if held_crypto._amount == 0 : #if no crypto in wallet
                        print(f'You have no {item[0]} to send.\n')
                    
                    elif held_crypto._blockchain == item[0] and held_crypto._amount > 0 : #if crypto in wallet
                        
                        max_amount = held_crypto._amount #max amount to send
                        
                        if item[1] > max_amount :
                            print(f'Failed send of {item[1]} {held_crypto._blockchain} to {to_address}. Requested amount exceeds holdings.\n')
                            return ValueError
                            break
                        
                        held_crypto._amount = round(held_crypto._amount - item[1], 5) #calculate new amount of asset in wallet, not value, just amount
                        print(f"Sent: {item[1]} of {held_crypto._blockchain} to '{to_address}'\n")
                    
                        #add transaction to transactions
                        transaction_info = (to_address, item)    
                        now = datetime.today().strftime('%Y-%m-%d - %H:%M:%S')
                        self._transactions.append([transaction_info, now, 's']) #s = send
                    
                        if held_crypto._amount < 0 :
                            held_crypto._amount = 0
                    else:
                        return ValueError
                        
        elif isinstance(obj, NFT):
            item.append(obj._title)
            item.append(obj._blockchain)
            item.append(obj._amount)
            item.append(obj._price)
            
            for held_nft in self._NFT_list :
                
                if item[0] == held_nft._title and item[1] == held_nft._blockchain and  held_nft._amount == 0: #if NFT already in wallet, but none available
                    print(f'You have no {item[0]} on {item[1]} to send.\n')
                    break
                    
                elif item[0] == held_nft._title and item[1] == held_nft._blockchain and held_nft.amount > 0 : #if NFT in wallet
                    
                    max_send = held_nft._amount #max amount to send
                    
                    if item[2] > max_send:
                        print(f'Failed send of {item[0]} on {item[1]} to {to_address}. Requested amount exceeds holdings.\n')
                        return ValueError
                        break
                    
                    held_nft._amount = held_nft._amount - item[2] #new amount in wallet
                    print(f"Sent: {item[2]} of {held_nft._title} to '{to_address}' on {held_nft._blockchain}\n")
                    
                    
                    #add transaction to transactions
                    transaction_info = (to_address, item)    
                    now = datetime.today().strftime('%Y-%m-%d - %H:%M:%S')
                    self._transactions.append([transaction_info, now, 's']) #s = send
                    
                    if held_nft._amount < 0 :
                        held_nft._amount = 0
                else: 
                    return ValueError
        else:
            return ValueError
        
        
        
    def spot_value(self, crypto) :
        """Returns spot price and value within wallet of a crypto.

        Args:
            crypto (str): cryptocurrency to find spot value of

        Returns:
            tuple: spot value, wallet value
        """
        if crypto in Wallet.acceptable_crypto :
            crypto = crypto.upper()
            url = "https://api.livecoinwatch.com/coins/single"
            payload = json.dumps({
                "currency" : "USD",
                "code" : crypto,
                "meta" : True
            })
            headers = {
                'content-type' : 'application/json',
                'x-api-key' : '6ad6bf16-aad3-48f4-ac1a-899bb4a7eb9e'
            }
        
            response = requests.request("POST", url, headers=headers, data=payload) #access API with spot price, returns JSON

            data = response.json()
            rate_value = round(data.get("rate"), 5)
        else :
            return 'Wallet does not support:', crypto
        
        
        #calculate value of crypto in wallet
        for item in self._crypto_list :
            if crypto.lower() == item._blockchain :
                v = rate_value * item._amount
            else :
                return rate_value, 0
                
        
        return rate_value, v  #tuple of spot price and value in wallet
                
                
    
    def print_items (self) :
        """Prints all items in wallet.
        """
        
        print("\n\tWALLET\n")
        
        print("Crypto\n")
        for item in self._crypto_list :
            print(f"Blockchain: {item._blockchain} \nAmount: {item._amount} \nAvg Price: {item._strike_price}\n")
            
        print("NFT\n")
        for item in self._NFT_list :
            print(f'Title: {item._title} \nBlockchain: {item._blockchain} \nAmount: {item._amount} \nAvg Price: {item._price}\n')
        
    
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

        
#TESTS
if __name__ == "__main__" :
    w1 = Wallet('1x0326')
    
    btc = Crypto('btc', 3, 40000)
    bag = NFT('bag', 'sol', 3, 10)
    bag2 = NFT('bag', 'sol', 2)
    
    w1.recieve('1x071', bag)
    w1.recieve('1x071', btc)
    
    w1.send('1x098', bag2)
    w1.send('1x098', ('btc', .5))
    
    btc2 = Crypto('btc', 10, 10000)
    w1.send('1x071', btc2)
        
    
    w1.print_items()
    
    
    btc_value = w1.spot_value('btc')
    eth_value = w1.spot_value('eth')
    
    print(btc_value[0], btc_value[1])
    print(eth_value[0], eth_value[1])
   


    print('\nTRANSACTIONS\n')

    print(w1._transactions, '\n')
    
    
    bonk = Crypto('bonk', 100, .01)
    print(w1.recieve('1x2345', bonk))
    
    