import bitcoin.wallet
from bitcoin.core import Hash160
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from bitcoin.core.key import CPubKey
from q1_p1 import generate_private_key, generate_public_key

bitcoin.SelectParams("testnet") # Select the network (testnet or mainnet)
my_private_key = bitcoin.wallet.CBitcoinSecret("923CPJacNiH4crjnz9hTH6cB7kb38CeiURRMoL1GTUFq9v64w8c") # Private key in WIF format XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('muUpXeFJEex17XMo6Pvh5CH6AeWPuaMsRj') # Destination address (recipient of the money)

private_key1 = bitcoin.wallet.CBitcoinSecret('923CPJacNiH4crjnz9hTH6cB7kb38CeiURRMoL1GTUFq9v64w8c')
private_key2 = bitcoin.wallet.CBitcoinSecret('93JBuQXNHqZpvAZ7ySzjQRENUfpP8FVge9EzmRmxmUYVKiUDAwj')
private_key3 = bitcoin.wallet.CBitcoinSecret('93Rpjdp6hmRJRHqwM9kUZy8Mr5L8y6eoSNmSS6u4xMstQVcAZQD')
public_key1: CPubKey = private_key1.pub
public_key2: CPubKey = private_key2.pub
public_key3: CPubKey = private_key3.pub


def P2MS_scriptPubKey(public_key1, public_key2, public_key3):
    return [OP_2, public_key1, public_key2, public_key3, OP_3, OP_CHECKMULTISIG]

def P2MS_scriptPubKey1(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2MS_scriptSig(txin, txout, txin_scriptPubKey):
    
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key] 

def send_from_P2MS_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)


    txin_scriptPubKey = P2MS_scriptPubKey1(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2MS_scriptSig(txin, [txout], txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_owned = 0. # BTC
    amount_to_send = 0.0155
    txid_to_spend = ('d663c44e16f30723dbdefff5c91b26133692930331e38d850bfc7488bfa79867') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print("address base58 =", my_address) # Prints your address in base58
    print("public key =",my_public_key.hex()) # Print your public key in hex
    print("private key =",my_private_key.hex()) # Print your private key in hex
    
    txout_scriptPubKey = P2MS_scriptPubKey(public_key1,public_key2,public_key3)
    print("txout scriptPubKey =",txout_scriptPubKey)
    response = send_from_P2MS_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    
    print("response status code =",response.status_code)
    print("response reason =", response.reason)
    print("Report:")
    print(response.text) # Report the hash of transaction which is printed in this section result
