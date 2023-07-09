import random


def negative_prompt_title() -> str:
    n = [
        'Uh oh!',
        'Would you look at that..',
        "Amazingly stupid",
        'Here you go, L',
        'Try using brain cells for once..',
        '"I pity you"',
        'Get good',
        'Critical hit!',
        'ooof!',
        'You truly deserve this..'
    ]
    return random.choices(n)


def positive_prompt_title() -> str:
    p = [
        'W moment',
        'Stupidly amazing!',
        'You are worthy..',
        'ok boomer',
        'I will take that as a compliment..',
        'slay on!',
        'ONG!',
        '+1',
        'Respect indeed',
        'Sun Tzu'
    ]
    return random.choices(p)

