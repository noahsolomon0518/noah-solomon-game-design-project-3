from sprites.enemies import *

level1_spawns = [
    [
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 10,
            "interval": 2
        }
    ],
    [
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 20,
            "interval": 1.8
        }
    ],
    [
        {
            "enemies":[Toad],
            "probabilities":[1],
            "amount": 10,
            "interval": 2.5
        },
        {
            "enemies":[Creature],
            "probabilities":[1],
            "amount": 1,
            "interval": 2.5
        },

    ]
]


level2_spawns = [
    [
        {
            "enemies":[Beholder],
            "probabilities":[1],
            "amount": 1,
            "interval": 2
        },
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 20,
            "interval": 2
        }
    ],
    [
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 20,
            "interval": 0.5
        }
    ],
    [
        {
            "enemies":[Toad, Mushrooms],
            "probabilities":[0.5,0.5],
            "amount": 20,
            "interval": 0.5
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 3,
            "interval": 5
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 1,
            "interval": 5
        },
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 30,
            "interval": 0.5
        }
    ],
    [
        {
            "enemies":[Bear, Mushrooms],
            "probabilities":[0.5, 0.5],
            "amount": 20,
            "interval": 3
        },
        {
            "enemies":[Toad],
            "probabilities":[1],
            "amount": 30,
            "interval": 0.2
        }
    ],
    [
        {
            "enemies":[Beholder],
            "probabilities":[1],
            "amount": 5,
            "interval": 3
        }
    ]
]