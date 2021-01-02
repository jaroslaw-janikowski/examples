#!/usr/bin/env python3

import sys
from libx11 import *


def main():
    display = XOpenDisplay(None)
    if not display:
        print('Cannot open display.')
        sys.exit(1)
    s = XDefaultScreen(display)
    w = XCreateSimpleWindow(display, RootWindow(d, s), 10, 10, 100, 100, 1, BlackPixel(display, s), WhitePixel(display, s))
    event = XEvent()
    XSelectInput(display, w, ExposureMask | ButtonPressMask)
    XMapWindow(display, w)

    while True:
        XNextEvent(display, byref(event))
        if event.type == Expose:
            XFillRectangle(display, w, DefaultGC(d, s), 20, 20, 10, 10)
            XDrawString(display, w, DefaultGC(d, s), 10, 50, msg, strlen(msg));
        elif event.type == ButtonPress:
            if event.xbutton.button == Button4:
                print('Scrolled up')
            elif event.xbutton.button == Button5:
                print('Scrolled down')
            else:
                print('cos')
    XCloseDisplay(display)

if __name__ == '__main__':
    main()
