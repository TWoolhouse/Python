def factor(a):
    return {i for i in range(1, a+1) if not a % i}

def in_all(*nums):
    fcts = [factor(i) for i in nums]
    return {i for i in range(1, sorted(nums)[-1]+1) if all((i in j for j in fcts))}

x = factor(40)
