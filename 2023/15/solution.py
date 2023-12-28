import sys
from dataclasses import dataclass

class Lens:
    """
    Each lens is a node in a doubly linked list.
    This allows maintaining the order of lenses,
    while also allowing for easy removal given a lens.
    """
    def __init__(self, label=None, focal_length=None, prev=None, next=None):
        self.label = label
        self.focal_length = focal_length
        self.prev = prev
        self.next = next

class Box:
    """
    Each box, labeled by its position in series, contains
    a doubly linked list of lenses and a hash map that maps
    lens labels (key) to the lens (value), which is a node
    in the doubly linked list.

    The hash map allows easy access for lens replacement or
    removal in the doubly linked list.
    """
    def __init__(self, number):
        self.number = number
        self.label2lens = {}
        # set up sentinels for linked list
        self.head_sentinel = Lens()
        self.tail_sentinel = Lens(prev=self.head_sentinel)
        self.head_sentinel.next = self.tail_sentinel

    def remove_lens(self, label):
        if label in self.label2lens:
            lens = self.label2lens.pop(label)
            # remove lens from doubly linked list
            lens.prev.next = lens.next
            lens.next.prev = lens.prev

    def add_lens(self, label, focal_length):
        if label in self.label2lens:
            # have lens with label already, so replace lens
            lens = self.label2lens[label]
            lens.focal_length = focal_length
        else:
            # need to insert lens. add to back
            tail = self.tail_sentinel.prev
            lens = Lens(
                label=label,
                focal_length=focal_length,
                prev=tail,
                next=self.tail_sentinel,
            )
            tail.next = lens
            self.tail_sentinel.prev = lens
            self.label2lens[label] = lens

    def compute_focusing_power(self):
        """
        For each lens, 
        power = (box_position+1) * slot * focal length
        e.g., for box 0 and a lens in the second slot with
        focal length 3,
        power = 1 * 2 * 3
        """
        power = 0
        slot = 1
        lens = self.head_sentinel.next
        while lens != self.tail_sentinel:
            power += (self.number+1) * slot * lens.focal_length
            slot += 1
            lens = lens.next
        return power

@dataclass
class Step:
    label: str
    operation: str
    focal_length: int = None

def read_input(input):
    with open(input, "r") as f:
        text = f.read().strip()
    words = text.split(",")
    return words

def get_ascii_code(char):
    return ord(char)

def HASH(char, start_val=0):
    val = start_val + get_ascii_code(char)
    val = val * 17
    val = val % 256
    return val

def hash_word(word):
    val = 0
    for char in word:
        val = HASH(char, val)
    return val

def process_words_into_steps(words):
    steps = []
    for word in words:
        if word[-1].isnumeric():
            focal_length = int(word[-1])
            operation = word[-2]
            label = word[:-2]
        else:
            focal_length = None
            operation = word[-1]
            label = word[:-1]
        step = Step(label, operation, focal_length)
        steps.append(step)
    return steps

def place_lenses(steps):
    # generate all of the boxes
    boxes = []
    for i in range(256):
        box = Box(i)
        boxes.append(box)
    # do each lens insertion/removal step
    for step in steps:
        # get correct box using HASH algorithm
        box_number = hash_word(step.label)
        box = boxes[box_number]
        # determine what to do based on operation
        if step.operation == "-":
            box.remove_lens(step.label)
        elif step.operation == "=":
            box.add_lens(step.label, step.focal_length)
    return boxes

def compute_focusing_power(boxes):
    power = 0
    for box in boxes:
        power += box.compute_focusing_power()
    return power

if __name__ == "__main__":
    words = read_input(sys.argv[1])
    val = 0
    for word in words:
        val += hash_word(word)
    print(val)

    steps = process_words_into_steps(words)
    boxes = place_lenses(steps)
    power = compute_focusing_power(boxes)
    print(power)

