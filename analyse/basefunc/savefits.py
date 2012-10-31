#! /usr/bin/env python
#-*- coding: utf-8 -*-

"""
Documents
"""

def savefits(hdu, path):
    hdu.writeto(path)
    return
