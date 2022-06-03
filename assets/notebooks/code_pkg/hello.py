import os

env_var = os.getenv("input")

def hello_world(v):
    print(v)

    
hello_world(env_var)
