def search_near(last: float, upper: float, down: float):
    res_upper = (abs(upper - last))
    res_down = abs(down - last)

    if res_upper < res_down:
        print(f'Upper - Last diff: {res_upper}')
        return res_upper, 'sell'
    else:
        print(f'Down - Last diff: {res_down}')
        return res_down, 'buy'
