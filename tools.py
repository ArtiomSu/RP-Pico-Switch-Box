import random

def generate_random_booleans(size, seed):
    # Set the random seed for reproducibility
    random.seed(seed)
    
    # Generate an array of random booleans
    random_booleans = [random.choice([True, False]) for _ in range(size)]
    
    return random_booleans

def get_last_output_sum(array):
    output = ""
    for i in range(len(array)):
        if array[i]:
            output = output + "1"
        else:
            output = output + "0"
    return output

