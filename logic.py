import random
from scipy.stats import truncnorm

# core
def core():
  # Mean and standard deviation of the distribution
  mean = 2
  std = 5

  # Lower and upper bounds of the distribution
  a = -200
  b = 200

  while True:
    # Generate a random number from the truncated normal distribution
    random_int = int(
      truncnorm((a - mean) / std, (b - mean) / std, loc=mean, scale=std).rvs())
    if -200 <= random_int <= 200:
      break
    else:
      continue

  if random_int < 0:  # For Negative value of random_int
    int2 = random.randint((random_int - 2), random_int)
    int1 = random_int - int2
    return random_int, int1, int2
  elif random_int > 0:  # For Positive value of random_int
    int1 = random.randint(random_int, (random_int + 2))
    int2 = random_int - int1
    return random_int, int1, int2
  elif random_int == 0:  # For Zero value of random_int
    while True:
      int1 = random.randint(1, 4)
      int2 = int1 * -1
      return random_int, int1, int2


# thread
def thread(int1, int2) -> int:
  kq = random.randint(0, 1)
  if int1+int2 > 0:
    ch = random.choice([kq, kq, kq , 0, 0, 0, 0])
  elif int1+int2 < 0:
    ch = random.choice([kq, kq, kq, 1, 1, 1, 1])  
  elif int1+int2 == 0:
    ch = random.randint(0,1)

  alt_int1 = 0
  alt_int2 = 0

  if ch == 1:

    z = random.randint(7, 20)

    if int1 == 0 or int2 == 0:
      int1 = int1 + z
      int2 = int2 - z
      p = random.randint(0, (-1 * int2))
      n = random.randint((int1 * -1), 0)
      alt_int1 = int1 + n
      alt_int2 = int2 + p
      alt_int = alt_int1 + alt_int2
      return alt_int, alt_int1, alt_int2

    if int1 == 0 and int2 == 0:
      alt_int1 = z
      alt_int2 = z * -1

      alt_int = alt_int1 + alt_int2
      return alt_int, alt_int1, alt_int2
    
    if int1 != 0 and int2 != 0:
        alt_int1 = int1 + random.randint(0, int1)
        alt_int2 = int2 - random.randint(int2, 0)
        alt_int = alt_int1 + alt_int2
        return alt_int, alt_int1, alt_int2  
  if ch == 0:

    z = random.randint(7, 20)

    if int1 == 0 or int2 == 0:
      int1 = int1 + z
      int2 = int2 - z
      p = random.randint((-1 * int1), 0)
      n = random.randint(0, (int2 * -1))

      alt_int1 = int1 + p
      alt_int2 = int2 + n

      alt_int = alt_int1 + alt_int2
      return alt_int, alt_int1, alt_int2
    
    if int1 == 0 and int2 == 0:
      alt_int1 = z
      alt_int2 = z * -1
      alt_int = alt_int1 + alt_int2
      return alt_int, alt_int1, alt_int2
    
    if int1 != 0 and int2 != 0:
        alt_int1 = int1 - random.randint(0, int1)
        alt_int2 = int2 + random.randint(int2, 0) 
        alt_int = alt_int1 + alt_int2
        return alt_int, alt_int1, alt_int2     