from typing import Tuple

def find_starting_code_number_for_band(band_number):
    """
    Find the starting code number given the band number.
    The first band starts at code number 1, the second
    at code number 2, the third at code number 4, etc.

    The iterative formula for the code number at the
    start of a band is the starting code number for
    the previous band plus the number of codes in that
    band:
    f(n) = f(n-1) + (n-1)
    where n is the band number and f(n) gives the starting
    code number for that band.
    """
    code_number = 1
    for i in range(1, band_number):
        code_number = code_number + i
    return code_number

def coordinates_to_code_number(coordinates: Tuple[int, int]) -> int:
    """
    Given a one-indexed coordinate, determine the number of
    the code it contains. For example, (1, 1) contains the
    first code and (4, 2) contains the 12th code.

    Because the codes are filled in diagonally up and to
    the right, a shortcut can be taken to find the number
    of the diagonal band it belongs to. For example,
    (1, 1) belongs to the 1st band. (4, 2) belongs to the
    5th band because the first band contained 1 item,
    the second contained 2, the third contained 3, and 
    the fourth contained 4.
    """
    row, col = coordinates
    band_number = row + col - 1
    number = col - 1 + find_starting_code_number_for_band(band_number)
    return number

def generate_next_code(code: int) -> int:
    return (code * 252533) % 33554393

def code_number_to_code(i: int) -> int:
    """
    Generate the code for the i-th code, which is one-indexed
    here. The first code is 20151125, as given by the prompt.
    To get the i-th code, the code generation formula needs
    to be applied i-1 times in succession.
    """
    code = 20151125 # 1st code
    for _ in range(i-1):
        code = generate_next_code(code)
    return code

def coordinates_to_code(coordinates: Tuple[int, int]) -> int:
    """
    Find the code number given its coordinate in the grid
    and then obtain the code by applying the code formula.
    """
    number = coordinates_to_code_number(coordinates)
    code = code_number_to_code(number)
    print(coordinates, number, code)
    return code

if __name__ == "__main__":
    target = (2981, 3075)
    # some test coordinates before computing the target
    coordinates = [(4,2), (3,4), (1, 6), (6, 5), target]
    for coord in coordinates:
        coordinates_to_code(coord)
