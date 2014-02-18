def print_summary(summary, prefix=''):
    parts = summary.split()
    while len(parts) > 0:
        print prefix,
        spaces = len(prefix)
        part = parts.pop(0)
        while True:
            print part,
            spaces += len(part) + 1
            if len(parts) == 0:
                break
            part = parts.pop(0)
            if len(part) + spaces > 72:
                print '\n%s' % prefix,
                spaces = len(prefix)
    print
