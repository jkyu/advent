def find_end_of_marker(
        buffer: str,
        marker_size: int = 4,
) -> int:
    """
    Find the 1-indexed position of the end of a marker,
    where a marker is a sequence of marker_size distinct
    characters.

    Find the marker by keeping track of all characters
    currently between the start of the marker and the
    cursor position. If a redundant character is found,
    move the marker start location up until the character
    the cursor is on is no longer redundant. Continue
    until a marker of the appropriate size is found.
    """
    marker = set()
    marker_start = cursor = 0
    while len(marker) < marker_size and cursor < len(buffer):
        if buffer[cursor] in marker:
            marker.remove(buffer[marker_start])
            marker_start += 1
        else:
            marker.add(buffer[cursor])
            cursor += 1
    return cursor


def read_input(file_name):
    with open(file_name, "r") as f:
        text = f.read().strip()
    return text


if __name__ == "__main__":
    sequence = read_input("input.txt")
    packet_start = find_end_of_marker(sequence, 4)
    print("Packet start:", packet_start)

    message_start = find_end_of_marker(sequence, 14)
    print("Message start:", message_start)
