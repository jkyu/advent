def look_and_say(sequence: str) -> str:
    new_sequence = []
    i = 0
    while i < len(sequence):
        count = 1
        while i+1 < len(sequence) and sequence[i+1] == sequence[i]:
            count += 1
            i += 1
        new_sequence.append(f"{count}{sequence[i]}")
        i += 1
    return "".join(new_sequence)

def repeat_look_and_say(sequence: str, n: int) -> str:
    for _ in range(n):
        sequence = look_and_say(sequence)
    return sequence

if __name__ == "__main__":
    new_sequence = repeat_look_and_say("1113222113", 40)
    print(len(new_sequence))

    new_sequence = repeat_look_and_say("1113222113", 50)
    print(len(new_sequence))