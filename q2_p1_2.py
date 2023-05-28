import bitcoin.wallet
from bitcoin.core import Hash160
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("93GFWshBtu4iSFwM6hVN5WcLSSD8sEpHWBhPpAnJwEgpCAEjaGd") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('mmir5fG6s4nDcVmiKveP92nkA7BD4sNLZK') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY ,OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key ] 

def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    # txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptPubKey = [OP_TRUE]
    txin_scriptSig = []

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    amount_owned = 0.017 # BTC
    amount_to_send = 0.016 # transaction fee = 0.017 - 0.016 = 0.001

    txid_to_spend = ('b9baa009551b44a091d4445be9bdf737afce282fa7c4620ffca5bcfbb4296974') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    

    print("address base58 =", my_address) # Prints your address in base58
    print("public key =",my_public_key.hex()) # Print your public key in hex
    print("private key =",my_private_key.hex()) # Print your private key in hex

    txout_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print("response status code =",response.status_code)
    print("response reason =", response.reason)
    print("Report:")
    print(response.text) # Report the hash of transaction which is printed in this section result
