"""
A dictionary containing the upper inclusive depth values as keys
We use the ceiling of the depth float to get the damage for that key
e.g., math.ceil(2.3) = 3, giving 95_000 for key 3 which spans 2 < d <= 3
"_" are ignored in Python, allowing for readability as a thousands separator
"""

damage_cost = {
    0: 0,
    1: 50_000,
    2: 80_000,
    3: 95_000,
    4: 105_000,
    5: 112_500,
    6: 120_000,
    7: 125_000,
    8: 130_000,
    9: 132_500,
    10: 134_000
}
