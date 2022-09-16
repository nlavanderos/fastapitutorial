def proceso(fnc):
    
    def wrapper(*args,**kwargs):
        exp1=list(map(fnc(),*args))
        return list(filter(lambda x:x is not None,exp1))

    return wrapper

@proceso
def filtro(*args):
    return lambda x:x if (x%2==0) else None

print(filtro([1,2,3,4,5,6]))

