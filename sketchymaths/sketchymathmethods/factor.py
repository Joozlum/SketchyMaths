def factor(number):
    result = []
    if number < 0:
        result.append(-1)
        number = abs(number)
    i = 1
    x = [1]
    while i*i <= number:
        for n in x:
            i += n
            while number % i == 0:
                result.append(i)
                number = number//i
        if number == 1:
            break
        if i == 3:
            x = [2]
        if i == 5:
            x = [2, 4]
    else:
        result.append(number)

    return tuple(result)