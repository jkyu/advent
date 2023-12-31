import math

def find_all_factors(number: int):
    """
    Find all factors of a number by starting at the square
    root and iterating down to 1.
    """
    factors = set()
    factor = int(round(math.sqrt(number)))
    while factor > 0:
        if number % factor == 0:
            factors.add(factor)
            factors.add(number // factor)
        factor -= 1
    return factors

def count_presents(house_number: int, limit: int = None):
    """
    An elf of number i delivers 10*i presents to each house
    whose number contains i as a factor. As a result, each
    house gets a number of presents equal to 10 times the 
    sum of its factors.

    If each elf stops delivering presents after a limit number
    of presents, the last house it delivers to is limit * i.
    As a result, a house only gets presents from elf i if
    house_number <= limit * i. From each elf, it gets 11 * i
    presents.
    """
    if limit is not None:
        total = 0
        factors = find_all_factors(house_number)
        for factor in factors:
            if factor * limit >= house_number:
                total += factor
        return 11 * total
    else:
        return 10 * sum(find_all_factors(house_number))

def find_smallest_house(
        target: int,
        initial_guess: int,
        limit: int = None,
    ) -> int:
    """
    Find the smallest house that gets a number of presents >= target.
    This can be solved by iterating up from 1, but this solutions 
    attempts to find the smallest house a bit faster by iterating up
    from an initial guess. Make sure no houses with number smaller
    than the initial guess can have presents >= target.

    An iteration limit of target/10 is used because the (target/10)-th
    elf will deliver target presents (target/10)-th house.
    """
    for house in range(initial_guess, target // 10):
        presents = count_presents(house, limit)
        if presents >= target:
            return house

if __name__ == "__main__":
    target_score = 29000000
    initial_guess = int(6e5)
    house = find_smallest_house(target_score, initial_guess)
    print(house)

    limit = 50
    house = find_smallest_house(target_score, initial_guess, limit)
    print(house)
