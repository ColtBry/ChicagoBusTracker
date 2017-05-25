def get_from_file(path):
    file = open(path, 'r').readlines()
    templates = {}

    template = ''
    for line in file:
        if line[0] == '#':
            if template != '':
                templates[name] = template
                template = ''
            name = line[1:-1].replace('#', '').strip()
        else:
            template += line

    templates[name] = template
    return templates