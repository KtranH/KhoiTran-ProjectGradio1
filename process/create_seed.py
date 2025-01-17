import random
def generate_random_seed():
    return random.randint(10000000000, 99999999999)
def update_seed():
    new_seed = generate_random_seed()
    return new_seed
