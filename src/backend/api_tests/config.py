BASE_URL = 'http://localhost:8080/api'

USERS = [
    {
        "telegramId": "123456789",
        "username": "johndoe",
        "avatarUrl": "https://example.com/johndoe_avatar.jpg"
    },
    {
        "telegramId": "987654321",
        "username": "jane_smith",
        "avatarUrl": "https://example.com/jane_smith_avatar.png"
    },
    {
        "telegramId": "456789123",
        "username": "peter_pan",
        "avatarUrl": "https://example.com/peter_pan_avatar.gif"
    },
    {
        "telegramId": "321987654",
        "username": "alice_wonderland",
        "avatarUrl": "https://example.com/alice_wonderland_avatar.svg"
    },
    {
        "telegramId": "654321987",
        "username": "bob_the_builder",
        "avatarUrl": "https://example.com/bob_the_builder_avatar.jpeg"
    }
]


MOVIES = [
    {
        "title": "The Cyberpunk Chronicles",
        "year": 2077,
        "image_url": "https://example.com/cyberpunk_chronicles.jpg",
        "genre": "Cyberpunk, Action, Sci-Fi",
        "description": "In a dystopian future, a skilled hacker fights against a mega-corporation that controls every aspect of life. He discovers a conspiracy that could change the world forever.",
        "duration": 120,
        "rating": 8.5,
        "user_added": True
    },
    {
        "title": "Mystic Forest: The Awakening",
        "year": 2023,
        "image_url": "https://example.com/mystic_forest.png",
        "genre": "Fantasy, Adventure, Family",
        "description": "A young girl discovers she has magical powers and must protect her village from an ancient evil that is awakening in the nearby mystic forest. She befriends talking animals and learns to control her abilities.",
        "duration": 95,
        "rating": 7.8,
        "user_added": False
    },
    {
        "title": "Space Explorers: Mission Nova",
        # "year": 2045,
        # "image_url": "https://example.com/space_explorers.gif",
        "genre": "Sci-Fi, Adventure, Thriller",
        # "description": "A team of astronauts embarks on a dangerous mission to colonize a newly discovered planet, Nova. They face unforeseen challenges, including hostile alien life and dwindling resources.",
        # "duration": 150,
        # "rating": 9.1,
        # "user_added": True
    },
    {
        "title": "Sunset Serenade",
        "year": 1998,
        "image_url": "https://example.com/sunset_serenade.jpeg",
        "genre": "Romance, Drama, Musical",
        "description": "Two musicians from different backgrounds fall in love while working on a project together. Their passion for music and each other is tested by their personal struggles and the pressures of the music industry.",
        "duration": 105,
        "rating": 6.9,
        "user_added": False
    },
    {
        "title": "The Haunted Mansion Mystery",
        "year": 2010,
        "image_url": "https://example.com/haunted_mansion.svg",
        "genre": "Horror, Mystery, Comedy",
        "description": "A group of teenagers accidentally stumbles upon a haunted mansion and must solve the mystery of the restless spirits that reside within before they become the next victims.",
        "duration": 88,
        "rating": 7.2,
        "user_added": True
    }
]


COLLECTIONS = [
    {
        "name": "Project Alpha",
        "description": "Discussion group for the Alpha project team.",
        "isDefault": False,
        "initialUsers": [
            {
                "telegramId": "111222333"
            },
            {
                "telegramId": "444555666"
            },
            {
                "telegramId": "777888999"
            }
        ]
    },
    {
        "name": "General Chat",
        "description": "General discussion for all users.",
        "isDefault": False,
    },
    {
        "name": "Marketing Team",
        "description": "Group for the marketing department.",
        "isDefault": False,
        "initialUsers": [
            {
                "telegramId": "222333444"
            },
            {
                "telegramId": "555666777"
            }
        ]
    },
    {
        "name": "Development Group",
        "description": "Technical discussions for the development team.",
        "isDefault": False,
        "initialUsers": [
            {
                "telegramId": "333444555"
            },
            {
                "telegramId": "666777888"
            }
        ]
    },
    {
        "name": "Beta Testers",
        "description": "Group for beta testers of the new application.",
        "isDefault": False,
        "initialUsers": [
            {
                "telegramId": "888999000"
            },
            {
                "telegramId": "999000111"
            },
            {
                "telegramId": "121314151"
            }
        ]
    }
]
