from pyglet.window import MouseCursor
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





level3_spawns = [
    [
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 20,
            "interval": 1
        }
    ],
    [
        {
            "enemies":[Mushrooms, Toad],
            "probabilities":[0.8,0.2],
            "amount": 20,
            "interval": 1.2
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 1,
            "interval": 0.1
        },
        {
            "enemies":[Mushrooms],
            "probabilities":[1],
            "amount": 25,
            "interval": 0.5
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 8,
            "interval": 3
        },
        {
            "enemies":[Beholder],
            "probabilities":[1],
            "amount": 1,
            "interval": 3
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 5,
            "interval": 0.5
        },
        {
            "enemies":[Toad],
            "probabilities":[1],
            "amount": 20,
            "interval": 0.5
        }
    ],
    [
        {
            "enemies":[Bear],
            "probabilities":[1],
            "amount": 20,
            "interval": 0.75
        }
    ],
    [
        {
            "enemies":[Bear, Beholder, Toad],
            "probabilities":[0.3,0.4,0.3],
            "amount": 60,
            "interval": 0.75
        }
    ],
    [
        {
            "enemies":[Necromancer],
            "probabilities":[1],
            "amount": 5,
            "interval": 1
        },
        {
            "enemies":[Toad, Mushrooms, Bear],
            "probabilities":[0.33,0.33,0.34],
            "amount": 75,
            "interval": 0.3
        }
    ],
    [
        {
            "enemies":[Necromancer],
            "probabilities":[1],
            "amount": 10,
            "interval": 0.75
        }
    ]
]