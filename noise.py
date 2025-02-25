from settings import SEED
from numba import njit
from opensimplex.internals import _noise2, _noise3, _init

# Initializes the permutation tables using the predefined seed
perm, perm_grad_index3 = _init(seed=SEED)

@njit(cache=True)
def noise2(x, y):
    """
    Generates 2D OpenSimplex noise.

    Parameters:
        x (float): The x-coordinate.
        y (float): The y-coordinate.

    Returns:
        float: Noise value at (x, y).
    """
    return _noise2(x, y, perm)

@njit(cache=True)
def noise3(x, y, z):
    """
    Generates 3D OpenSimplex noise.

    Parameters:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
        z (float): The z-coordinate.

    Returns:
        float: Noise value at (x, y, z).
    """
    return _noise3(x, y, z, perm, perm_grad_index3)
