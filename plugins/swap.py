#!/usr/bin/env python

import psutil

import plugins


class Plugin(plugins.BasePlugin):


    def run(self, *unused):
        swap = {}
        mem = psutil.swap_memory()
        for name in mem._fields:
            swap[name] = getattr(mem, name)
        return swap


if __name__ == '__main__':
    Plugin().execute()
