import pprint


def read_alg():
    with open('./data/20a.csv') as f:
        r = f.readline()
        assert len(r[:-1]) == 512
        return r[:-1]


def read_img():
    with open('./data/20b.csv') as f:
        img = []
        for line in f.readlines():
            img.append(line[:-1])
        return img


def pad_img(img: list[str, ...], char: str = '.'):
    new_img = [char*(len(img[0]) + 2)] + [char + line + char for line in img] + [char*(len(img[0]) + 2)]
    for x in new_img:
        assert len(new_img[0]) == len(x)
    return new_img


def enhance(img: list[str,...], padding: str = '.'):
    padded = pad_img(pad_img(img, padding), padding)
    alg = read_alg()
    new_img = []
    for i in range(1, len(padded)-1):
        new_line = [""] * (len(padded[0]))
        for j in range(1, len(padded[0]) - 1):
            nghbrs = padded[i-1][j-1:j+2] + padded[i][j-1:j+2] + padded[i+1][j-1:j+2]
            indx = "".join(['1' if x == '#' else '0' for x in nghbrs ])
            new_line[j] = alg[int(indx, 2)]
        new_img.append("".join(new_line))
    return new_img


def first():
    im = enhance(read_img())
    # im = enhance(["...", "...", "..."])
    im = enhance(im, "#")
    counter = 0
    for x in im:
        print(x)
        for c in x:
            if c == '#':
                counter += 1
    print(counter)


def second():
    im = read_img()
    # im = ["...", "...", "..."]
    pad = '.'
    for k in range(50):
        im = enhance(im, pad)
        if pad == '.':
            pad = '#'
        else:
            pad = '.'
    counter = 0
    for x in im:
        print(x)
        for c in x:
            if c == '#':
                counter += 1
    print(counter)


second()