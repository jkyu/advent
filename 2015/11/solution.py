def is_valid_password(password: str) -> bool:
    # rule 1: must have a three character straight
    codes = [ord(x) for x in password]
    has_straight = False
    for i in range(2, len(password)):
        if codes[i] - codes[i-1] == 1 and codes[i-1] - codes[i-2] == 1:
            has_straight = True
    if not has_straight:
        return False
    # rule 2: already implemented during password generation
    # rule 3: must have at least two non-overlapping doubles
    count = 0
    i = 1
    while i < len(password):
        if password[i] == password[i-1]:
            count += 1
            # skips the next character to ensure that
            # doubles do not overlap
            i += 1
        i += 1
    if count < 2:
        return False
    return True

def find_next_password(password: str):
    """
    Increment rightmost character. If "z" was
    incremented, reset the character to "a" and
    move one character to the left.

    Skip any password that contains disallowed
    characters to slightly improve the speed
    of the brute force search.
    """
    ref = ord("a")
    disallowed_values = {
        ord(x)-ref for x in ["i", "o", "l"]
    }
    codes = [ord(x)-ref for x in password]
    i = len(codes)-1
    while i >= 0:
        codes[i] += 1
        # do not bother attempting passwords with
        # disallowed characters
        if codes[i] in disallowed_values:
            codes[i] += 1
        if codes[i] % 26 == 0:
            codes[i] = 0
            i -= 1
        else:
            break
    new_password = "".join([chr(x+ref) for x in codes])
    return new_password

def find_next_valid_password(password: str):
    """
    Loop until another valid password is found.
    The initial password may be valid, so start
    validation checks with the next potential
    password.
    """
    password = find_next_password(password)
    while not is_valid_password(password):
        password = find_next_password(password)
    return password

if __name__ == "__main__":
    current_password = "hepxcrrq"
    new_password = find_next_valid_password(current_password)
    print(new_password)

    new_password = find_next_valid_password(new_password)
    print(new_password)