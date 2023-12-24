import sys

from dataclasses import dataclass
from scipy import optimize
from typing import List, Tuple

@dataclass
class Stone:
    position: Tuple[int]
    velocity: Tuple[int]

def read_input(input: str) -> List[Stone]:
    with open(input, "r") as f:
        lines = f.read().strip().splitlines()
    stones = []
    for line in lines:
        position, velocity = [x.strip() for x in line.split("@")]
        px, py, pz = [int(x.strip()) for x in position.split(",")]
        vx, vy, vz = [int(x.strip()) for x in velocity.split(",")]
        stones.append(Stone((px, py, pz), (vx, vy, vz)))
    return stones

def in_bounds(val, bounds):
    return bounds[0] <= val <= bounds[1]

def has_intersection(stonei, stonej, bounds):
    """
    Solve system of two equations for times for which two stones
    reach the same position (possibly not simultaneously). Ensure
    the intersection times are positive and that the intersection
    is within the boundaries.

    For the ith and jth stones, the shared intersection point is:
    x = ti*vxi + xi = tj*vxj + xj
    y = ti*vyi + yi = tj*vyj + yj

    We need to find the times ti and tj to ensure they are both
    positive (intersection occurs in the future) and then determine
    whether the intersection (x, y) is in the boundary box.
    """
    try:
        xi, yi, zi = stonei.position
        xj, yj, zj = stonej.position
        vxi, vyi, vzi = stonei.velocity
        vxj, vyj, vzj = stonej.velocity
        # check if stone i at time ti is at the same
        # position as stone j at time tj
        tj = (xi*vyi + vxi*yj - vxi*yi - xj*vyi) / (vyi*vxj - vxi*vyj)
        ti = (yj + vyj*tj - yi) / vyi
        # now find that position
        x = ti*vxi + xi
        y = ti*vyi + yi
        return in_bounds(x, bounds) and in_bounds(y, bounds) and ti >= 0 and tj >= 0
    except ZeroDivisionError:
        return False

def count_intersections(stones, bounds):
    """Check intersection for all pairs of stones"""
    intersections = 0
    for i in range(len(stones)):
        for j in range(i+1, len(stones)):
            if has_intersection(stones[i], stones[j], bounds):
                intersections += 1
    return intersections

def find_intersecting_line(stones):
    """
    We want to find a line with starting position
    (x, y, z) and velocity (vx, vy, vz) such that
    it has an intersection with the ith stone at 
    some time ti.

    This gives us three equations for each stone:
    x + vx*ti = xi + vxi*ti
    y + vy*ti = yi + vzi*ti
    z + vz*ti = zi + vzi*ti
    This system has seven unknowns:
    (x, y, z, vx, vy, vz, ti)
    It is therefore underdetermined. However, including
    additional stones only introduces one more unknown 
    (the time) with three more equations, since the 
    starting position and velocity of the thrown rock
    are shared.

    Then we can get a fully-determined system of equations
    by including three stones:
    x + vx*ti = xi + vxi*ti
    y + vy*ti = yi + vzi*ti
    z + vz*ti = zi + vzi*ti
    x + vx*tj = xj + vxj*tj
    y + vy*tj = yj + vzj*tj
    z + vz*tj = zj + vzj*tj
    x + vx*tk = xk + vxk*tk
    y + vy*tk = yk + vzk*tk
    z + vz*tk = zk + vzk*tk

    We can solve this system of equations to obtain
    (x, y, z) and (vx, vy, vz).

    With all of the stones, we have an overdetermined
    system of equations. We only need three stones to
    find (x, y, z) and (vx, vy, vz) for all of the stones.
    (including more stones will help us find ti for
    each, but that is irrelevant for the problem).
    For this reason, we arbitrarily pick three
    stones to solve for the position and velocity of
    the thrown rock.

    To improve the numerical stability of the nonlinear
    solver we'll throw at these equations, we can reduce
    the number of parameters further by eliminating the 
    time variables since they are irrelevant. Doing so
    yields six equations to solve for six unknowns:

    (x - xi)*(vy - vyi) = (y - yi)*(vx - vxi)
    (x - xi)*(vz - vzi) = (z - zi)*(vx - vxi)
    (x - xj)*(vy - vyj) = (y - yj)*(vx - vxj)
    (x - xj)*(vz - vzj) = (z - zj)*(vx - vxj)
    (x - xk)*(vy - vyk) = (y - yk)*(vx - vxk)
    (x - xk)*(vz - vzk) = (z - zk)*(vx - vxk)

    Due to possibile stability or rounding issues in 
    scipy.optimize.fsolve, it may be a good idea to
    try a few different rocks (and maybe a different
    initial guess).
    """
    def equations(parameters):
        x, y, z, vx, vy, vz = parameters
        equations = []
        for i in range(3):
            xi, yi, zi = stones[i].position
            vxi, vyi, vzi = stones[i].velocity
            equations.append((x-xi)*(vy-vyi) - (y-yi)*(vx-vxi))
            equations.append((x-xi)*(vz-vzi) - (z-zi)*(vx-vxi))
        return equations
    # use the last stone as an initial guess for the solver
    initial_guess = stones[-1].position + stones[-1].velocity
    solution = optimize.fsolve(equations, initial_guess)
    thrown_rock = Stone(
        (solution[0], solution[1], solution[2]),
        (solution[3], solution[4], solution[5])
    )
    return thrown_rock

if __name__ == "__main__":
    stones = read_input(sys.argv[1])
    # bounds = (7, 27)
    bounds = (200000000000000, 400000000000000)
    intersections = count_intersections(stones, bounds)
    print(intersections)

    rock = find_intersecting_line(stones)
    print(rock)
    print(round(sum(rock.position)))
