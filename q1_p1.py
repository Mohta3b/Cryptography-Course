import hashlib
import base58
import random
import ecdsa
import codecs
import colorama

num_of_private_key_bits = 256

def generate_private_key():
    # Generate a random 256-bit number (32 bytes)
    random_number = random.getrandbits(256)
    private_key = random_number.to_bytes(32, byteorder="big")

    # Add test network prefix (0xEF) to the private key
    private_key_extended = b'\xEF' + private_key

    # Calculate the double SHA256 hash of the extended private key
    hash1 = hashlib.sha256(private_key_extended).digest()
    hash2 = hashlib.sha256(hash1).digest()

    # Take the first 4 bytes of the double hash as the checksum
    checksum = hash2[:4]

    # Append the checksum to the extended private key
    private_key_with_checksum = private_key_extended + checksum

    # Convert the extended private key to Base58 format (Wallet Import Format - WIF)
    wif = base58.b58encode(private_key_with_checksum).decode('utf-8')
 
    return private_key, wif

def generate_public_key(private_key):
    public_key_raw = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = public_key_raw.to_string()

    public_key_hex = codecs.encode(public_key_bytes, 'hex')

    # Add public key prefix (0x04) to the start of the public key
    public_key_bit = (b'04' + public_key_hex).decode("utf-8")

    hex_str = bytearray.fromhex(public_key_bit)

    # Derive the public key from the uncompressed public key
    public_key = hashlib.sha256(hex_str).digest()

    # Calculate the RIPEMD-160 hash of the public key
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(public_key)
    hash3 = ripemd160.digest()

    # Add test network prefix (0x6F) to the hash
    hash_with_prefix = b'\x6F' + hash3

    # Calculate the double SHA256 hash of the hash with prefix
    hash4 = hashlib.sha256(hash_with_prefix).digest()
    hash5 = hashlib.sha256(hash4).digest()

    # Take the first 4 bytes of the double hash as the checksum
    checksum = hash5[:4]
    # print("checksum: ", checksum)

    # Append the checksum to the hash with prefix
    hash_with_prefix_and_checksum = hash_with_prefix + checksum

    # Convert the hash with prefix and checksum to Base58 format (Test network address)
    address = base58.b58encode(hash_with_prefix_and_checksum)

    return address

if __name__ == '__main__':
    private_key, wif = generate_private_key()

    public_key = generate_public_key(private_key)

    print("WIF:\n" + colorama.Back.BLUE + wif + colorama.Back.RESET)
    print("Public key:\n" + colorama.Back.GREEN + public_key + colorama.Back.RESET)