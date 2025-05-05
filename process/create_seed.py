import random
def generate_random_seed():
    return random.randint(1000000000000, 9999999999999)
def update_seed():
    new_seed = generate_random_seed()
    return new_seed
