def read(loc: str) -> list:
    with open(loc) as f:
        r = f.readlines()
        data = [[int(x, 2) for x in row.strip()] for row in r]
        return data


def first(loc: str = "./data/3.csv") -> int:
    data = read(loc)

    sums = [0] * len(data[0])
    for row in data:
        for column, val in enumerate(row):
            sums[column] += val

    gamma = "".join([str(int(k > len(data) // 2)) for k in sums])
    epsilon = "".join('1' if x == '0' else '0' for x in gamma)

    res = int(gamma, 2) * int(epsilon, 2)
    print(res)
    return res


def second(loc: str = "./data/3.csv") -> int:
    data = read(loc)
    nums = data

    # oxygen / most common bit
    k = 0
    while len(nums) > 1:
        sums = sum(row[k] for row in nums)
        bit: int = int(sums >= (len(nums) + 1) // 2)
        nums = list(filter(lambda l: l[k] == bit, nums))
        k += 1
    assert len(nums) == 1
    oxygen_rating = int("".join(map(str,nums[0])), 2)

    # CO2 scrubber rating / least common bit
    nums = data
    k = 0
    while len(nums) > 1:
        sums = sum(row[k] for row in nums)
        bit: int = int(sums < len(nums) // 2)
        nums = list(filter(lambda l: l[k] == bit, nums))
        k += 1
    assert len(nums) == 1
    co2_rating = int("".join(map(str,nums[0])), 2)

    res = oxygen_rating * co2_rating 
    print(res)
    return res


first()
second()
