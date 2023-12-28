import hashlib

def find_number(secret_key, prefix="00000"):
    """
    Brute force search for number that pairs with
    the secret key to give an MD5 hash with the
    required prefix of zeros.
    """
    i = 1
    while True:
        key = f"{secret_key}{i}"
        md5_hash = hashlib.md5(key.encode())
        if md5_hash.hexdigest().startswith(prefix):
            return i
        i += 1

if __name__ == "__main__":
    secret_key = "bgvyzdsv"
    # hash starts with 5 zeros
    number = find_number(secret_key, "00000")
    print(number)

    # hash starts with 6 zeros
    number = find_number(secret_key, "000000")
    print(number)
