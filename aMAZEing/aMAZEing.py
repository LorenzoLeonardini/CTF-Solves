from __future__ import print_function
from pwn import *
from PIL import Image
import numpy
import maze as solver
import sys

sys.setrecursionlimit(10000000)

conn = remote('139.59.30.165', 9300)
while True:
    line = conn.recvline(timeout=4)
    if('Enter)' in line):
        conn.recvline()
        break
    # print(line.replace('\n', ''))
conn.send('\n')

while True:
    ff = open('image.png', 'w+')
    while True:
        f = conn.recvline(timeout=4)
        # print(f)
        ff.write(bytearray(f))
        if 'Give us the path or write INVALID' in f:
            break;
    ff.close()


    im = Image.open('image.png')
    im = im.resize((im.width / 10, im.height / 10), Image.NEAREST)
    im.save('resized.png')
    im_arr = numpy.array(im)
    im.close()
    # print(im_arr)

    maze = []
    ll = ''
    for i in range(0, im.height + 2):
        ll += '#'
    maze.append(ll)
    for line in im_arr:
        l = '#'
        for pixel in line:
            if pixel[0] == 0:
                l += '#'
            else:
                l += ' '
        l += '#'
        maze.append(l)
    maze.append(ll)
    maze[1] = '#S' + maze[1][2:]
    maze[im.height] = maze[im.height][:-2] + 'E#'

    # maze_file = open('maze.txt', 'w+')
    # for i in maze:
    #     for j in i:
    #         maze_file.write(j)
    #     maze_file.write('\n')
    # maze_file.close()

    maze_obj = solver.Maze()
    maze_obj.read_personal(maze)
    solution = solver.solve(maze_obj)
    if solution:
        # print("\n\tI HAVE THE SOLUTION!\n")
        # maze_obj.write_file('solution.txt')
        conn.send(maze_obj.return_solution() + '\n')
    else:
        # print("\n\tI DON'T HAVE THE SOLUTION!\n")
        conn.send('INVALID\n')

    while conn.can_recv(timeout=4):
        readed = conn.recvline(timeout=4)
        # print(readed)
        if 'WooHoo you got it correct. Now solve a few more and get your flag.' in readed:
            break

    finished = False

    while True:
        readed = conn.recvline(timeout=4)
        if 'PNG' in readed:
            conn.unrecv(readed)
            break
        elif 'Congratulations' in readed:
            print(readed, end='')
            finished = True
            break

    if finished:
        break
