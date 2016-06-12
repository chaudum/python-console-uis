#!/usr/bin/env python

import curses
import subprocess
from datetime import datetime


class CursesScreen:

    def __enter__(self):
        self.stdscr = curses.initscr()
        curses.start_color()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(1)
        return self.stdscr

    def __exit__(self, a, b, c):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()


def show_whoami(screen, pad_l, pad_r):
    whoami = subprocess.check_output(["whoami"])
    pwd = subprocess.check_output(["pwd"])
    pad_l.clear()
    pad_l.addstr(1, 1, "You are logged in as:")
    pad_l.addstr(2, 1, whoami.decode('utf-8'))
    pad_l.addstr(4, 1, "Your working directory is:")
    pad_l.addstr(5, 1, pwd.decode('utf-8'))
    pad_l.refresh()

def show_time(screen, pad_l, pad_r):
    now = datetime.now().isoformat()
    pad_l.clear()
    pad_l.addstr(1, 1, "The current time is:")
    pad_l.addstr(2, 1, now)
    pad_l.refresh()

def show_line_col(screen, pad_b):
    y, x = screen.getyx()
    pad_b.clear()
    pad_b.addstr(0, 2, "line: {} column: {}".format(y, x))
    pad_b.refresh()

def main(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_WHITE)

    my, mx = screen.getmaxyx()

    pad_l = screen.subpad(my, int(mx/2), 0, 0)
    pad_l.bkgdset(curses.color_pair(5))
    pad_l.clear()
    pad_l.refresh()

    pad_r = screen.subpad(my, int(mx/2), 0, int(mx/2))
    pad_r.border(0)
    pad_r.addstr(1, 2, '1')
    pad_r.addstr(1, 4, 'whoami', curses.color_pair(2))
    pad_r.addstr(2, 2, '2')
    pad_r.addstr(2, 4, 'time', curses.color_pair(3))
    pad_r.addstr(3, 2, 'q')
    pad_r.addstr(3, 4, 'quit', curses.color_pair(1))
    pad_r.refresh()

    pad_b = screen.subpad(1, int(mx/2)-2, my-2, int(mx/2)+1)
    pad_b.bkgdset(curses.color_pair(4))
    show_line_col(screen, pad_b)

    while True:
        y, x = screen.getyx()
        key = screen.getch()
        if key == ord('1'):
            show_whoami(screen, pad_l, pad_r)
        elif key == ord('2'):
            show_time(screen, pad_l, pad_r)
        elif key == curses.KEY_LEFT:
            screen.move(y, max(0, min(x-1, int(mx/2)-1)))
        elif key == curses.KEY_RIGHT:
            screen.move(y, max(0, min(x+1, int(mx/2)-1)))
        elif key == curses.KEY_UP:
            screen.move(max(0, min(y-1, my-1)), x)
        elif key == curses.KEY_DOWN:
            screen.move(max(0, min(y+1, my-1)), x)
        elif key == ord('q'):
            break
        show_line_col(screen, pad_b)


if __name__ == '__main__':
    with CursesScreen() as scr:
        try:
            main(scr)
        except KeyboardInterrupt:
            pass

