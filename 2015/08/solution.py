import sys

def read_input(file):
    with open(file, "r") as f:
        lines = f.read().strip().splitlines()
    words = []
    for line in lines:
        words.append(line.strip())
    return words

def decode(word):
    # remove start and end quotes
    word = word[1:-1]
    i = 0
    chars = []
    while i < len(word):
        if word[i] == "\\":
            # case: \\ should turn into \
            if word[i+1] == "\\":
                chars.append("\\")
                i += 2
            # case: \" should turn into "
            elif word[i+1] == '"':
                chars.append('"')
                i += 2
            # case: \xab should turn into int(chr(ab, 16))
            elif word[i+1] == "x":
                hex_code = word[i+2:i+4]
                chars.append("*")
                # chars.append(chr(int(hex_code, 16)))
                i += 4
        else:
            chars.append(word[i])
            i += 1
    new_word = "".join(chars)
    return new_word

def encode(word):
    i = 0
    chars = []
    while i < len(word):
        # if we see a backslash, escape it
        if word[i] == "\\":
            chars.append("\\\\")
        # if we see a double quote, escape it
        elif word[i] == '"':
            chars.append('\\"')
        else:
            chars.append(word[i])
        i += 1
    # add the start and end quotes
    new_word = "".join(['"'] + chars + ['"'])
    return new_word

def difference_after_decoding(words):
    difference = 0
    for word in words:
        new_word = decode(word)
        difference += len(word) - len(new_word)
    return difference

def difference_after_encoding(words):
    difference = 0
    for word in words:
        new_word = encode(word)
        difference += len(new_word) - len(word)
    return difference

if __name__ == "__main__":
    words = read_input(sys.argv[1])
    difference = difference_after_decoding(words)
    print(difference)
    difference = difference_after_encoding(words)
    print(difference)
