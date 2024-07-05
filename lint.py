#!/usr/bin/env python3
import glob, pathlib, re, sys

def error(counter, path, row, message):
    sys.stderr.write(f'{path}:{row}: {message}\n')
    counter[0] += 1

counter = [0]
for path in glob.glob('**', recursive=True):
    if not re.fullmatch(r'System/.*\.hsc?', path):
        continue
    contents = pathlib.Path(path).read_text()

    for i, line in enumerate(contents.splitlines()):
        if len(line) > 80:
            error(counter, path, i+1, f'line over 80 chars')

    contents = re.sub(r'--.*', '', contents)
    for m in re.finditer(r'(?s)\b(os|so)\b\s*(\S*)', contents):
        func, next_token = m.groups()
        if not re.fullmatch(r'|'.join([
                r'".*',
                r'=',
                r'::',
                r'EXE_EXTENSION',
                r'.*exeExtension',
        ]), next_token):
            row = 1 + contents[:m.start()].count('\n')
            error(counter, path, row, f'{func} only allowed on literals')
if counter[0]:
    sys.exit(f'{counter[0]} error(s)')
