import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("91fDSsw2BjQkLzunYJJuYFfuU7BFxxV7bmSCevNdvWpoiEzzuBn") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('mmirxVXgCxyWMdXr3AH3zUift4RJegHxbj') # Destination address (recipient of the money)

def P2PKH_scriptPubKey(address):
    ######################################################################
    ## Fill out the operations for P2PKH scriptPubKey                   ##
    return [OP_DUP, OP_HASH160, Hash160(address), OP_EQUALVERIFY ,OP_CHECKSIG]
    ######################################################################

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key ] 

def send_from_P2PKH_transaction(amount_to_send1,
                                amount_to_send2,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey):
    txout1 = create_txout(amount_to_send1, txout_scriptPubKey)
    txout2 = create_txout(amount_to_send2, [OP_FALSE])


    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, [txout1, txout2], txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout1, txout2], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_owned = 0.007 # BTC
    amount_to_send = 0.006
    txid_to_spend = ('2b83e1c8a381acee46e837ca8d94a9eb2d0f8a3a31132de83aaa7c68b0b432f3') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print("address base58 =", my_address) # Prints your address in base58
    print("public key =",my_public_key.hex()) # Print your public key in hex
    print("private key =",my_private_key.hex()) # Print your private key in hex
    
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    
    print("response status code =",response.status_code)
    print("response reason =", response.reason)
    print("Report:")
    print(response.text) # Report the hash of transaction which is printed in this section result
