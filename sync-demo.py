#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Keep this repo's demo.svg in step with its source.

The profile README embeds a copy of the status line render. The source of truth
is `claude-statusline/docs/demo.svg`, produced by that project's own
`docs/make_demo.py` from a real render. This script copies it here so the two
never drift.

    python3 sync-demo.py            # copy when changed
    python3 sync-demo.py --check    # change nothing; exit 1 if stale

Run it after regenerating the demo, then commit both repos.
"""
import sys, io, os, shutil, hashlib

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(HERE, 'demo.svg')
# Sibling project by default; override with --source for a different layout.
DEFAULT_SOURCE = os.path.join(os.path.dirname(HERE), 'claude-statusline', 'docs', 'demo.svg')


def digest(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except OSError:
        return None


def main():
    args = sys.argv[1:]
    check_only = '--check' in args
    source = DEFAULT_SOURCE
    if '--source' in args:
        source = args[args.index('--source') + 1]

    src_sum = digest(source)
    if src_sum is None:
        sys.exit('source not found: %s\n'
                 '(expected the claude-statusline repo next to this one, '
                 'or pass --source PATH)' % source)

    dst_sum = digest(DEST)
    if src_sum == dst_sum:
        print('demo.svg is up to date (%s)' % src_sum[:12])
        return 0

    if check_only:
        print('demo.svg is STALE (source %s, local %s)'
              % (src_sum[:12], (dst_sum or 'missing')[:12]))
        return 1

    shutil.copy2(source, DEST)
    print('demo.svg updated: %s -> %s' % ((dst_sum or 'missing')[:12], src_sum[:12]))
    print('now commit it:  git add demo.svg && git commit -m "Sync demo image"')
    return 0


if __name__ == '__main__':
    sys.exit(main())
