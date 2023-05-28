from q1_p1 import generate_private_key, generate_public_key
import colorama

def generate_vanity_address(vanity_letters):
    vanity_len = len(vanity_letters)
    count = 0
    ten_thousand_count = 0
    while(True):
        if count == 10000:
            ten_thousand_count += 1
            print(f'{ten_thousand_count}0,000 addresses generated so far!')
            count = 0
        test_private_key , test_wif = generate_private_key()
        test_public_key = generate_public_key(test_private_key)MIR
        
        if test_public_key[1:vanity_len+1] == vanity_letters:
            print("Found vanity address after "+ str(ten_thousand_count * 10000 + count) + " attempts!")
            return test_public_key, test_wif
        count += 1
        
if __name__ == '__main__':
    vanity_str = input()
    vanity_address, vanity_wif = generate_vanity_address(vanity_letters=vanity_str)
    print("Vanity Address:" , colorama.Back.BLUE +  vanity_address + colorama.Back.RESET)
    print("Vanity Private Key (WIF):" , colorama.Back.GREEN +  vanity_wif + colorama.Back.RESET)