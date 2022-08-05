def read(loc: str) -> tuple[str, list[str]]:
    with open(loc) as f:
        r = f.readlines()
        alg = r[0].strip()
        img = [row.strip() for row in r[2:]]
    return alg, img


def pad_img(img: list[str], pad: str = '.'):
    new_img = [pad*(len(img[0]) + 2)] + [pad + line + pad for line in img] + [pad*(len(img[0]) + 2)]
    return new_img


def enhance(alg: str, img: list[str], padding: str = '.'):
    padded = pad_img(pad_img(img, padding), padding) # Pad twice
    new_img = []
    for i in range(1, len(padded)-1):
        new_line = [""] * len(padded[0])
        for j in range(1, len(padded[0]) - 1):
            nghbrs = padded[i-1][j-1:j+2] + padded[i][j-1:j+2] + padded[i+1][j-1:j+2]
            indx = "".join(['1' if x == '#' else '0' for x in nghbrs ])
            new_line[j] = alg[int(indx, 2)]
        new_img.append("".join(new_line))
    return new_img


def print_image(img: list[str]):
    print(f"Printing image of dimensions: x: {len(img[0])}, y: {len(img)}")
    for row in img:
        assert len(row) == len(img[0])
        print(len(row), row)


def iterate_enhance(alg: str, img: list[str], n: int) -> list[str]:
    pads = {
            '.': alg[0],
            '#': alg[-1],
            }
    pad = '.'
    for _ in range(n):
        img = enhance(alg, img, pad)
        pad = pads[pad]
    return img


def count_lit_pixels(img: list[str]) -> int:
    return sum(row.count("#") for row in img)


def first(loc: str = "./data/20.txt") -> int:
    alg, img = read(loc)
    img = iterate_enhance(alg, img, 2)
    counter = count_lit_pixels(img)
    print(counter)
    return counter


def second(loc: str = "./data/20.txt") -> int:
    alg, img = read(loc)
    img = iterate_enhance(alg, img, 50)
    counter = count_lit_pixels(img)
    print(counter)
    return counter



if __name__ == '__main__':
    first("./data/20test.txt")
    second("./data/20test.txt")
    first()
    second()
