#!/usr/bin/env python3

from ctypes import *
from ctypes.wintypes import DWORD, HWND, HANDLE, LPCWSTR, WPARAM, LPARAM, RECT, POINT, MSG


WSTRING = c_wchar_p
LPWSTR = WSTRING

def MAKEINTRESOURCEW(i):
    return LPWSTR(i)

WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000
SW_SHOWNORMAL = 1
SW_SHOW = 5
CS_HREDRAW = 2
CS_VREDRAW = 1
CW_USEDEFAULT = 0x80000000
WM_DESTROY = 2
WM_PAINT = 7
WHITE_BRUSH = 0
IDI_APPLICATION = MAKEINTRESOURCEW(32512)
IDC_ARROW = MAKEINTRESOURCEW(32512)
COLOR_WINDOW = 5


class WNDCLASSEX(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("style", c_uint),
        ("lpfnWndProc", WNDPROCTYPE),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HANDLE),
        ("hIcon", HANDLE),
        ("hCursor", HANDLE),
        ("hBrush", HANDLE),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
        ("hIconSm", HANDLE)
    ]


szWindowClass = "win32app"
szTitle = "Win32 Guided Tour Application"
hInst = None


def WndProc(hWnd, message, wParam, lParam):
    ps = None
    hdc = None
    greeting = "Hello, World!"

    if message == WM_PAINT:
        hdc = windll.user32.BeginPaint(hWnd, ps)
        windll.gdi32.TextOutW(hdc, 5, 5, greeting, len(greeting))
        windll.user32.EndPaint(hWnd, ps)
    elif message == WM_DESTROY:
        windll.user32.PostQuitMessage(0)
    else:
        return windll.user32.DefWindowProcW(hWnd, message, wParam, lParam)
    return 0;


def WinMain(hInstance, hPrevInstance, lpCmdLine, nCmdShow):
    wcex = WNDCLASSEX()
    wcex.cbSize = sizeof(WNDCLASSEX);
    wcex.style          = CS_HREDRAW | CS_VREDRAW
    wcex.lpfnWndProc    = WNDPROCTYPE(WndProc)
    wcex.cbClsExtra     = 0
    wcex.cbWndExtra     = 0
    wcex.hInstance      = hInstance
    wcex.hIcon          = windll.user32.LoadIconW(hInstance, IDI_APPLICATION)
    wcex.hCursor        = windll.user32.LoadCursorW(None, IDC_ARROW)
    wcex.hbrBackground  = COLOR_WINDOW+1
    wcex.lpszMenuName   = None
    wcex.lpszClassName  = szWindowClass
    wcex.hIconSm        = windll.user32.LoadIconW(wcex.hInstance, IDI_APPLICATION)
    msg = MSG()
    hInst = hInstance

    if not windll.user32.RegisterClassExW(byref(wcex)):
        windll.user32.MessageBox(None, "Call to RegisterClassEx failed!", "Win32 Guided Tour", 0)
        return 1

    hWnd = windll.user32.CreateWindowExW(
        0,
        szWindowClass,
        szTitle,
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT,
        500, 100,
        None,
        None,
        hInstance,
        None
    )

    if not hWnd:
        windll.user32.MessageBox(None, "Call to CreateWindow failed!", "Win32 Guided Tour", 0)
        return 1

    windll.user32.ShowWindow(hWnd, nCmdShow)
    windll.user32.UpdateWindow(hWnd)

    lpmsg = pointer(msg)
    while windll.user32.GetMessageA(lpmsg, 0, 0, 0):
        windll.user32.TranslateMessage(lpmsg)
        windll.user32.DispatchMessageA(lpmsg)

    return int(msg.wParam)

if __name__ == '__main__':
    WinMain(windll.kernel32.GetModuleHandleW(0), None, None, True)
