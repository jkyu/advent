import re
import sys

def read_input(file):
    with open(file, "r") as f:
        text = f.read().strip()
    replacements, molecule = text.split("\n\n")
    replacement_map = {}
    reduction_map = {}
    for line in replacements.splitlines():
        element, substitute = [x.strip() for x in line.split(" => ")]
        if element not in replacement_map:
            replacement_map[element] = set()
        replacement_map[element].add(substitute)
        reduction_map[substitute] = element
    return replacement_map, reduction_map, molecule.strip()

def generate_molecules(molecule, replacements):
    """
    Generate all new molecules that can be formed by replacing
    a single element with an allowed substitute.
    """
    new_molecules = set()
    i = 0
    while i < len(molecule):
        if molecule[i] in replacements:
            for substitute in replacements[molecule[i]]:
                new_molecule = molecule[:i] + substitute + molecule[i+1:]
                new_molecules.add(new_molecule)
        elif i+1 < len(molecule):
            element = molecule[i:i+2]
            if element in replacements:
                for substitute in replacements[element]:
                    new_molecule = molecule[:i] + substitute + molecule[i+2:]
                    new_molecules.add(new_molecule)
                i += 1
        i += 1
    return new_molecules

def reduce_molecule(molecule, reductions):
    """
    Since each replacement is done in isolation to generate the molecule
    and there are no replacement options that subsume others or idempotent
    replacements, a greedy approach can be used to reduce the final molecule
    to an electron by performing all replacements in reverse. At any time,
    perform the first allowed reverse replacement until self-consistency
    is reached (at which point no more replacements are allowed). This
    will end up as a single electron.
    """
    steps = 0
    last = None
    while molecule != last:
        last = molecule
        for substitute, element in reductions.items():
            if substitute in molecule:
                steps += 1
                molecule = re.sub(substitute, element, molecule, count=1)
    return steps

if __name__ == "__main__":
    replacements, reductions, molecule = read_input(sys.argv[1])
    new_molecules = generate_molecules(molecule, replacements)
    print(len(new_molecules))

    steps_to_reduce = reduce_molecule(molecule, reductions)
    print(steps_to_reduce)
