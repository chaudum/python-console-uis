#!/usr/bin/env python3
# example1.py

import curses

stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

try:
    height, width = stdscr.getmaxyx()
    num = min(height, width)
    for x in range(num):
        stdscr.addch(x, x, 'x')

    stdscr.addstr(3, 3, "Hello Vorarlberg Webdev Meetup")

    for x in range(8):
        stdscr.addch(4, x, curses.ACS_HLINE)
    stdscr.addch(4, 8, curses.ACS_PLUS)
    stdscr.addch(4, 9, curses.ACS_LRCORNER)

    stdscr.refresh()
    key = None
    while not key or key not in [ord('q'), ord('Q')]:
        key = stdscr.getch()
        stdscr.addch(4, 10, key)
        stdscr.refresh()
except KeyboardInterrupt:
    pass
finally:
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

