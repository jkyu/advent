import sys

from collections import Counter

def read_input(input):
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    return lines

def does_not_contain_bad_string(string):
    bad_strings = {"ab", "cd", "pq", "xy"}
    for bad in bad_strings:
        if bad in string:
            return False
    return True

def has_vowel_requirement(string):
    vowels = {"a", "e", "i", "o", "u"}
    letters = Counter(string)
    n_vowels = 0
    for vowel in vowels:
        n_vowels += letters.get(vowel, 0)
    return n_vowels >= 3

def has_repeat_letter(string):
    for i in range(1, len(string)):
        if string[i] == string[i-1]:
            return True
    return False

def has_repeat_letter_with_buffer(string):
    for i in range(2, len(string)):
        if string[i-2] == string[i]:
            return True
    return False

def has_repeating_pair(string):
    pairs = {}
    for i in range(1, len(string)):
        pair = string[i-1:i+1]
        if pair not in pairs:
            pairs[pair] = i
        # does not share a letter, like in aaa
        elif pairs[pair] != i-1:
            return True
    return False

def is_nice(string, better_model):
    if better_model:
        return has_repeating_pair(string) and has_repeat_letter_with_buffer(string)
    else:
        return has_vowel_requirement(string) and has_repeat_letter(string) and does_not_contain_bad_string(string)

def count_nice_strings(strings, better_model=False):
    nice_strings = 0
    for string in strings:
        if is_nice(string, better_model):
            nice_strings += 1
    return nice_strings

if __name__ == "__main__":
    lines = read_input(sys.argv[1])
    nice_strings = count_nice_strings(lines)
    print(nice_strings)

    nice_strings = count_nice_strings(lines, True)
    print(nice_strings)
