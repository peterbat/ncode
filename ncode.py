#!/usr/bin/python

import sys, re, string, random, os
import termios, fcntl, struct

def get_term_width():
    if len(sys.argv) == 2:
        return int(sys.argv[1])
    s = struct.pack("HHHH", 0, 0, 0, 0)
    fd_stdout = sys.stdout.fileno()
    x = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, s)
    rows, cols, xp, yp = struct.unpack("HHHH", x)
    return cols

#dark = "@#$%&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
#light = ",.+-;:!^()\\|/<>`~'"
dark = "@#$%&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
light = ",.+-;:!^()\\|/`~'"

alphabet_width = 13
alphabet_height = 5
alphabet = {
        'a' : "0000011100000"\
              "0000110110000"\
              "0001111111000"\
              "0011000001100"\
              "0011000001100",
        'b' : "0001111111000"\
              "0001100001100"\
              "0001111111000"\
              "0001100001100"\
              "0001111111000",
        'c' : "0000111111000"\
              "0001100001100"\
              "0011000000000"\
              "0001100001100"\
              "0000111111000",
        'd' : "0001111111000"\
              "0001100001100"\
              "0001100000110"\
              "0001100001100"\
              "0001111111000",
        'e' : "0001111111100"\
              "0001100000000"\
              "0001111111000"\
              "0001100000000"\
              "0001111111100",
        'f' : "0001111111100"\
              "0001100000000"\
              "0001111111000"\
              "0001100000000"\
              "0001100000000",
        'g' : "0000111111000"\
              "0001100000000"\
              "0011000111100"\
              "0001100001100"\
              "0000111111000",
        'h' : "0001100001100"\
              "0001100001100"\
              "0001111111100"\
              "0001100001100"\
              "0001100001100",
        'i' : "0001111111100"\
              "0000001100000"\
              "0000001100000"\
              "0000001100000"\
              "0001111111100",
        'j' : "0001111111100"\
              "0000000110000"\
              "0000000110000"\
              "0001100110000"\
              "0000111110000",
        'k' : "0001100011000"\
              "0001100110000"\
              "0001111100000"\
              "0001100110000"\
              "0001100011100",
        'l' : "0001100000000"\
              "0001100000000"\
              "0001100000000"\
              "0001100000000"\
              "0001111111100",
        'm' : "0001100011000"\
              "0011010101100"\
              "0011001001100"\
              "0110000000110"\
              "0110000000110",
        'n' : "0001100001100"\
              "0001111001100"\
              "0001101101100"\
              "0001100111100"\
              "0001100001100",
        'o' : "0000111111000"\
              "0001100001100"\
              "0011000000110"\
              "0001100001100"\
              "0000111111000",
        'p' : "0001111111000"\
              "0001100001100"\
              "0001111111000"\
              "0001100000000"\
              "0001100000000",
        'q' : "0000111111000"\
              "0001100001100"\
              "0011001110110"\
              "0001100011100"\
              "0000111111110",
        'r' : "0001111110000"\
              "0001100001100"\
              "0001111110000"\
              "0001100110000"\
              "0001100011100",
        's' : "0001111111100"\
              "0011000000000"\
              "0001111110000"\
              "0000000001100"\
              "0011111111000",
        't' : "0001111111100"\
              "0000001100000"\
              "0000001100000"\
              "0000001100000"\
              "0000001100000",
        'u' : "0011000001100"\
              "0011000001100"\
              "0011000001100"\
              "0011000001100"\
              "0001111111000",
        'v' : "0011000001100"\
              "0011000001100"\
              "0001100011000"\
              "0000110110000"\
              "0000011100000",
        'w' : "0110000000110"\
              "0110000000110"\
              "0011001001100"\
              "0011010101100"\
              "0001100011000",
        'x' : "0011000001100"\
              "0001100011000"\
              "0000111110000"\
              "0001100011000"\
              "0011000001100",
        'y' : "0011000011000"\
              "0001100110000"\
              "0000111100000"\
              "0000011000000"\
              "0000011000000",
        'z' : "0011111111100"\
              "0000000110000"\
              "0000011000000"\
              "0001100000000"\
              "0011111111100"}

def get_character(b):
    if b == '0':
        return light[random.randint(0, len(light) - 1)]
    elif b == '1':
        return dark[random.randint(0, len(dark) - 1)]

def transform_row(r):
    return ''.join([get_character(c) for c in r])

def sanitize_text(s):
    # Remove all non-alpha characters from s.
    pattern = re.compile('[^A-Za-z]+')
    return pattern.sub('', s).lower()

def get_one_line(s):
    strans = sanitize_text(s)
    # Construct the lines of strans.
    lines = [""] * alphabet_height
    for i in range(alphabet_height):
        for j in range(len(strans)):
            lines[i] += transform_row(alphabet[strans[j]][i * alphabet_width : (i + 1) * alphabet_width])
    w = len(lines[0])
    lines.insert(0,transform_row("0" * w))
    lines.append(transform_row("0" * w))
    return '\n'.join(lines)

def print_one_line(s):
  print(get_one_line(s))

def chunks(l, n):
    for i in range(0, len(l), n):
        end = i + n
        if i == n - 1 and ((len(l) % n) != 0):
            end = i + (len(l) % n) + 1
        yield l[i : end]

def get_message(m, columns=-1):
    m_san = sanitize_text(m)
    if columns < alphabet_width:
      cols = get_term_width()
    else:
      cols = columns
    nblocks = int(cols / alphabet_width)
    lines = chunks(m_san, nblocks)
    message = []
    for l in lines:
        message.append(get_one_line(l))
    return '\n'.join(message)

def print_message(m):
  print(get_message(m))

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line)
    message = ''.join(lines)
    print_message(message)

if __name__ == '__main__':
    main()
