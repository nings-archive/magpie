#!/usr/bin/env python3

import os, sys
import magpie.core

def expand_paths(path_list):
    expanded_paths = []
    working_dir = os.getcwd() + '/'
    for path in path_list:
        if path[0] == '/':
            expanded_paths.append(path)
        else:
            expanded_paths.append(working_dir + path)
    return expanded_paths

core = magpie.core.Core()
args = sys.argv[1:]
document_paths = expand_paths(args)
if len(document_paths) == 0:
    sys.stderr.write("fetch: missing file operands\n")
    sys.stdout.write("  Try: fetch [FILE]...\n")
for path in document_paths:
    core.send_document(path)
