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

prime_number1 = 1009
prime_number2 = 1861


def P2MS_scriptPubKey(public_key):
    return [OP_DUP, OP_HASH160, Hash160(public_key), OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptPubKey(public_key):
    sum = prime_number2 + prime_number1
    sub = prime_number2 - prime_number1
    return [OP_2DUP, OP_SUB, OP_HASH160, Hash160(sub.to_bytes(2, byteorder='little')), OP_EQUALVERIFY,
            OP_ADD, OP_HASH160, Hash160(sum.to_bytes(2, byteorder='little')), OP_EQUAL]


def P2MS_scriptSig(txin, txout, txin_scriptPubKey):
    
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)
    
    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)


    txin_scriptPubKey = P2PKH_scriptPubKey(my_public_key)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = [prime_number2, prime_number1]

    new_tx = create_signed_transaction(txin, [txout], txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)


if __name__ == '__main__':
    ######################################################################
    amount_owned = 0.0145 # BTC
    amount_to_send = 0.014
    txid_to_spend = ('7246d433b0730ea74a4b8ff985a28cb2232dd9a80ddffbf14d61ca242b66f26c') # TxHash of UTXO
    utxo_index = 0 # UTXO index among transaction outputs
    ######################################################################

    print("address base58 =", my_address) # Prints your address in base58
    print("public key =",my_public_key.hex()) # Print your public key in hex
    print("private key =",my_private_key.hex()) # Print your private key in hex
    
    txout_scriptPubKey = P2MS_scriptPubKey(my_public_key)
    
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    
    print("response status code =",response.status_code)
    print("response reason =", response.reason)
    print("Report:")
    print(response.text) # Report the hash of transaction which is printed in this section result
