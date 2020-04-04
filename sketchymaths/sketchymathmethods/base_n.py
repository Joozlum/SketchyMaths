def split_divide(number, base):
    x = number // base
    r = number % base
    result = [r]
    if x:
        if x >= base:
            result.extend(split_divide(x, base))
        else:
            result.append(x)
    return result

def base_n(number, base):
    result = split_divide(number, base)
    result.reverse()
    result = ':'.join([str(x) for x in result])
    result += f'b{base}'
    return result

