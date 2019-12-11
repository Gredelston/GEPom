#!/usr/bin/env python3
import curses

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, 'Hello, curses!')
    for i in range(1, 11):
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(i, 10./i))

    stdscr.refresh()
    stdscr.getkey()


if __name__ == '__main__':
    curses.wrapper(main)
