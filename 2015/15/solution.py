import sys

from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple

@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

def read_input(file: str):
    with open(file, "r") as f:
        text = f.read().strip().splitlines()
    ingredients= {}
    for line in text:
        name, parameters = line.split(": ")
        parameters = parameters.split(", ")
        property_values = [int(x.split()[1]) for x in parameters]
        ingredient = Ingredient(name, *property_values)
        ingredients[name] = ingredient
    return ingredients

def compute_property(
        ingredients: Dict[str, Ingredient],
        ingredient_counts: Dict[str, int],
        property: str,
    ) -> int:
    """
    Returns the total property value after considering
    all ingredients.
    """
    property_value = 0
    for name, count in ingredient_counts.items():
        property_value += count * getattr(ingredients[name], property)
    return max(property_value, 0)

def score_function(
        ingredients: Dict[str, Ingredient],
        ingredient_counts: Dict[str, int],
        properties: List[str],
    ) -> int:
    """
    Returns the score as a product of the property values over
    all of the ingredients.
    """
    score = 1
    for property in properties:
        score *= compute_property(ingredients, ingredient_counts, property)
    return score

def find_optimal_combination(
        ingredients: Dict[str, Ingredient],
        properties: List[str],
        combinations: Iterator[Tuple[int, ...]],
        calorie_limit: Optional[int] = None,
    ):
    """
    Brute force discovery of the best scoring cookie.
    """
    best_score = 0
    for ingredient_combination in combinations:
        ingredient_counts = {}
        for name, count in zip(ingredients.keys(), ingredient_combination):
            ingredient_counts[name] = count
        if calorie_limit is not None:
            calories = compute_property(ingredients, ingredient_counts, "calories")
            if calories != calorie_limit:
                continue
        score = score_function(ingredients, ingredient_counts, properties)
        if score > best_score:
            best_score = score
    return best_score

def ingredient_combination_generator(
        limit: int = 100,
    ) -> Iterator[Tuple[int, int, int, int]]:
    for sugar in range(limit+1):
        for sprinkles in range(limit+1):
            for candy in range(limit+1):
                chocolate = 100 - sugar - sprinkles - candy
                if chocolate < 0:
                    continue
                yield sugar, sprinkles, candy, chocolate

if __name__ == "__main__":
    ingredients = read_input(sys.argv[1])
    properties = ["capacity", "durability", "flavor", "texture"]

    combinations = ingredient_combination_generator(100)
    best_score = find_optimal_combination(ingredients, properties, combinations)
    print(best_score)

    combinations = ingredient_combination_generator(100)
    best_score = find_optimal_combination(
        ingredients,
        properties,
        combinations,
        calorie_limit=500,
    )
    print(best_score)
