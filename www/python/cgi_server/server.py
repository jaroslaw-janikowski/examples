#!/usr/bin/env python

import BaseHTTPServer
import SimpleHTTPServer
import CGIHTTPServer

if __name__ == '__main__':
    SimpleHTTPServer.test(
        CGIHTTPServer.CGIHTTPRequestHandler, BaseHTTPServer.HTTPServer)
