
'\nsample test\n'

@test_sample_before(ceshi1='ceshi', ceshi2=1)
@testing
@test_sample(ceshi1='ceshi', ceshi2=1, ceshi3=True, ceshi4={'ceshi': 'ceshi', 'ceshi2': 1, 1: 'ceshi3'}, ceshi5=[1, 2, 'ceshi'], ceshi6=(1, 2), ceshi7=5.6, ceshi8=9j)
@ceshi1
def add(arg1, arg2):
    if (arg1 == 1):
        return (arg1 + arg2)
    else:
        return arg1

@ceshi3
def delete(arg1, arg2):
    if (arg1 == 1):
        return (arg1 - arg2)
    else:
        return arg1
