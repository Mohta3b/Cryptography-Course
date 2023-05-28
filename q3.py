import time,struct
import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x, Hash
from utils import *
from bitcoin.core.key import CPubKey
from bitcoin.core import Hash160

BLOCK_REWARD = 6.25

bitcoin.SelectParams('mainnet')
my_private_key = bitcoin.wallet.CBitcoinSecret('KynBR8eAQSjDEj4CvUEzqdD9TpbZi4cdXr6iQnPV4xE4wB3tzw71')
my_public_key: CPubKey = my_private_key.pub # 1DvvDsThneeAAKrKqzvMe4P4Dy395pWCJa


def P2PKH_scriptPubKey(my_public_key):
    return [OP_DUP, OP_HASH160, Hash160(my_public_key),OP_EQUALVERIFY ,OP_CHECKSIG]


def get_target(bits):
    exponent = int(bits[:2], 16)
    coefficient = int(bits[2:], 16)
    target = coefficient * (2 ** (8 * (exponent - 3)))
    target_hexpadded = f'{target:x}'.zfill(64)
    return bytes.fromhex(target_hexpadded)


def coinbaseTransaction(BLOCK_REWARD, coinbase_txid_to_spend, coinbase_utxo_index,
        output_script, coinbase_script_sig):
    txin = create_txin(coinbase_txid_to_spend, coinbase_utxo_index)
    txout = create_txout(BLOCK_REWARD, output_script)
    txin.scriptSig = coinbase_script_sig
    return CMutableTransaction([txin], [txout])

def get_merkleRoot(coinbase_tx):
    merkle_root = b2lx(Hash(coinbase_tx.serialize()))
    return merkle_root, coinbase_tx.serialize()


def get_partial_header(block_version, last_block_hash, merkle_root, bits):
    time_ = int(time.time())
    time_ = struct.pack('<L', time_)
    return struct.pack('<L', block_version) + lx(last_block_hash)[::-1] + lx(merkle_root)[::-1] + time_ + bytes.fromhex(bits)[::-1]

def mine_block(partial_header, target):
    nonce = 0
    while True:
        header = partial_header + struct.pack('<L', nonce)
        block_hash = Hash(header)
        if block_hash < target:
            print("Nonce used: ", nonce)
            return header, block_hash
        nonce += 1

def mine(last_block_hash, coinbase_data_hex):
    bits = '1f010000'
    target = get_target(bits)
    coinbase_tx = coinbaseTransaction(BLOCK_REWARD, last_block_hash, 0, P2PKH_scriptPubKey(my_public_key), [coinbase_data_hex])
    merkle_root, coinbase_tx_serialized = get_merkleRoot(coinbase_tx)
    partial_header = get_partial_header(1, last_block_hash, merkle_root, bits)
    header, block_hash = mine_block(partial_header, target)
    return header, block_hash, coinbase_tx_serialized




if __name__ == '__main__':
    # for student id 81019(9511)
    last_block_hash = "00000000faac558a7a5266c3c678e53b53b88a619b00dd825395b8e4ca44cdd9"
    coin_base_data = "810199511AmirAliVahidi"
    coin_base_data_hex = coin_base_data.encode('utf-8').hex()
    header, block_hash, block_body = mine(last_block_hash, coin_base_data_hex)
    
    print("Block hash: ", b2lx(block_hash))
    print("Block header: ", b2x(header))
    print("Block body: ", b2x(block_body))
    print("Block size: ", len(header) + len(block_body))
    print("Block reward: ", BLOCK_REWARD)
    print("Block version: ", 1)
    
