from ansible import errors


def mongo_filter(arg, family='rhel', os_v='5', mongo_v='3.6.0'):
    result = ''
    print family
    if family == 'RedHat':
        family = 'rhel'

    family_v = family+os_v
    for x in arg:
        if all((family_v in x, mongo_v in x)):
            result = x
            break
    return result


class FilterModule(object):
    def filters(self):
        return {
            'mongo_filter': mongo_filter
        }
