from ctypes import c_bool, c_char_p, c_double, c_float, c_int, c_uint, c_ulong, c_void_p, cdll, POINTER
from tkinter import Tk, YES, BOTH, Frame

_xlib = cdll.LoadLibrary('libX11.so.6')
_gl = cdll.LoadLibrary('libGL.so')

# Data types for Linux Platform
XID = c_ulong
GLXDrawable = XID

# Data types for OpenGL
GLbitfield = c_uint
GLubyte = c_char_p
GLclampf = c_float
GLclampd = c_double
GLdouble = c_double
GLenum = c_uint
GLfloat = c_float
GLint = c_int

GL_BLEND = 0x0BE2
GL_COLOR_BUFFER_BIT = 0x00004000
GL_DEPTH_BUFFER_BIT = 0x00000100
GL_DEPTH_TEST = 0x0B71
GL_MODELVIEW = 0x1700
GL_ONE_MINUS_SRC_ALPHA = 0x0303
GL_PROJECTION = 0x1701
GL_QUADS = 0x0007
GL_RENDERER = 0x1F01
GL_SRC_ALPHA = 0x0302
GL_VENDOR = 0x1F00
GL_VERSION = 0x1F02
GL_TRUE = 1

# Constants for Linux Platform
PGLint = GLint * 15

GLX_RGBA = 4
GLX_RED_SIZE = 8
GLX_GREEN_SIZE = 9
GLX_BLUE_SIZE = 10
GLX_DEPTH_SIZE = 12
GLX_DOUBLEBUFFER = 5

# OpenGL Function Definitions
glBegin = _gl.glBegin
glBegin.restype = None
glBegin.argtypes = [GLenum]

glClear = _gl.glClear
glClear.restype = None
glClear.argtypes = [GLbitfield]

glBlendFunc = _gl.glBlendFunc
glBlendFunc.restype = None
glBlendFunc.argtypes = [GLenum, GLenum]

glClearColor = _gl.glClearColor
glClearColor.restype = None
glClearColor.argtypes = [GLclampf, GLclampf, GLclampf, GLclampf]

glClearDepth = _gl.glClearDepth
glClearDepth.restype = None
glClearDepth.argtypes = [GLclampd]

glColor3f = _gl.glColor3f
glColor3f.restype = None
glColor3f.argtypes = [GLfloat, GLfloat, GLfloat]

glEnable = _gl.glEnable
glEnable.restype = None
glEnable.argtypes = [GLenum]

glEnd = _gl.glEnd
glEnd.restype = None
glEnd.argtypes = None

glFlush = _gl.glFlush
glFlush.restype = None
glFlush.argtypes = None

glGetString = _gl.glGetString
glGetString.restype = GLubyte
glGetString.argtypes = [GLenum]

glLoadIdentity = _gl.glLoadIdentity
glLoadIdentity.restype = None
glLoadIdentity.argtypes = None

glMatrixMode = _gl.glMatrixMode
glMatrixMode.restype = None
glMatrixMode.argtypes = None

glOrtho = _gl.glOrtho
glOrtho.restype = None
glOrtho.argtypes = [GLdouble, GLdouble, GLdouble, GLdouble, GLdouble, GLdouble]

glRotatef = _gl.glRotatef
glRotatef.restype = None
glRotatef.argtypes = [GLfloat, GLfloat, GLfloat, GLfloat]

glVertex3f = _gl.glVertex3f
glVertex3f.restype = None
glVertex3f.argtypes = [GLfloat, GLfloat, GLfloat]

glViewport = _gl.glViewport
glViewport.restype = None
glViewport.argtypes = [GLint, GLint, GLint, GLint]

glXChooseVisual = _gl.glXChooseVisual
glXChooseVisual.argtypes = [c_void_p, c_int, POINTER(c_int)]
glXChooseVisual.restype = c_void_p

glXCreateContext = _gl.glXCreateContext
glXCreateContext.argtypes = [c_void_p, c_void_p, c_void_p, c_bool]
glXCreateContext.restype = c_void_p

glXMakeCurrent = _gl.glXMakeCurrent
glXMakeCurrent.argtypes = [c_void_p, GLXDrawable, c_void_p]
glXMakeCurrent.restype = c_bool

glXSwapBuffers = _gl.glXSwapBuffers
glXSwapBuffers.argtypes = [c_void_p, GLXDrawable]
glXSwapBuffers.resttype = None

X11_None = 0

x_open_display = _xlib.XOpenDisplay
x_open_display.argtypes = [c_char_p]
x_open_display.restype = c_void_p


class TkOglWin(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title(kwargs.get('app_title', 'Opengl Test'))
        self.bind('<Configure>', self.on_resize)
        self.parent.after(100, self._cfg_tkogl)

    def _cfg_tkogl(self):
        att = PGLint(
            GLX_RGBA, 1,
            GLX_DOUBLEBUFFER, 1,
            GLX_RED_SIZE, 4,
            GLX_GREEN_SIZE, 4,
            GLX_BLUE_SIZE, 4,
            GLX_DEPTH_SIZE, 16,
            X11_None
        )

        self.dpy = x_open_display(None)
        vi = glXChooseVisual(self.dpy, 0, att)
        glc = glXCreateContext(self.dpy, vi, None, GL_TRUE)
        glXMakeCurrent(self.dpy, self.winfo_id(), glc)
        self.set_ortho_view()
        self.parent.after(10, self._render_loop)

    def on_resize(self, event, arg=None):
        raise NotImplementedError

    def _render_loop(self):
        self.render_scene()
        glXSwapBuffers(self.dpy, self.winfo_id())
        self.parent.after(5, self._render_loop)

    def render_scene(self):
        raise NotImplementedError

    def set_ortho_view(self):
        raise NotImplementedError


class AppOgl(TkOglWin):
    rot = 0

    def on_resize(self, event, arg=None):
        if event:
            w = event.width
            h = event.height
        else:
            if arg:
                w = arg['w']
                h = arg['h']
            else:
                raise Exception

        dx = w / h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2 * dx, 2 * dx, -2, 2, -2, 2)

    def set_ortho_view(self):
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor(0, 0, 0, 0)
        glClearDepth(1)
        glMatrixMode(GL_PROJECTION)

        self.on_resize(None, arg={
            'w': self.winfo_width(),
            'h': self.winfo_height()
        })

        print('%s - %s - %s' % (
            glGetString(GL_VENDOR),
            glGetString(GL_VERSION),
            glGetString(GL_RENDERER)
        ))

    def render_scene(self):
        self.rot += .5

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(self.rot, 1, 1, 0.5)

        # Draw a simple cube.
        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glVertex3f(1, 1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glColor3f(1, 0.5, 0)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glColor3f(1, 0, 0)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glColor3f(1, 1, 0)
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glColor3f(0, 0, 1)
        glVertex3f(-1, 1, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glColor3f(1, 0, 1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)
        glEnd()
        glFlush()

if __name__ == '__main__':
    root = Tk()
    app = AppOgl(root, width=320, height=200)
    app.pack(fill=BOTH, expand=YES)
    app.mainloop()
