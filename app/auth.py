import random
import time

def generate_token(username: str) -> str:
    r = random.randint(0, 10000000) 
    t = int(time.time())
    return f"{username}-{t}-{r}"
