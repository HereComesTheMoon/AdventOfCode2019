import csv

def first():
    count = 0
    with open("./data/day1.csv") as f:
        reader = csv.reader(f)
        last = int(reader.__next__()[0])
        for x in reader:
            x = int(x[0])
            if x > last:
                count += 1
            last = x
    return count


def second():
    with open("./data/day1.csv") as f:
        data = [int(x[0]) for x in csv.reader(f)]
        print(data)

    count = 0
    current = data[0]+data[1]+data[2]
    last = current
    for i in range(3, len(data)):
        current = current + data[i] - data[i-3]
        if current > last:
            count += 1
        last = current

    return count

print(first())
print(second())