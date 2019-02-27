def test(condition, e):
    if not condition:
        print(e)


"""
两个入参， 一个结果 的测试
"""
func2 = (lambda x, y: y)
params2 = [
    [([1, 3, 5, 6], 5), 2],
    [([1, 3, 5, 6], 2), 1],
    [([1, 3, 5, 6], 0), 0],
    [([1, 3, 5, 6], 7), 4],
]


def two_param_to_test(_function, _params):
    for index, i in enumerate(_params):
        param1 = i[0][0]
        param2 = i[0][1]
        exp = i[1]
        test(_function(param1, param2) == exp, f'err{index}: -{i}')


two_param_to_test(func2, params2)


"""
一个入参, 一个结果， 的测试
"""

func1 = (lambda y: y)
params1 = [
    [([1, 3, 5, 6],), 2],
    [([1, 3, 5, 6],), 1],
    [([1, 3, 5, 6],), 0],
    [([1, 3, 5, 6],), 4],
]


def one_param_to_test(_function, _params):
    for index, i in enumerate(_params):
        param1 = i[0][0]
        exp = i[1]
        test(_function(param1) == exp, f'err{index}: -{i}')


one_param_to_test(func1, params1)
