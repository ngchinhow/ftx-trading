from decimal import Decimal


def do_ema(new_input, old_ema, old_var, alpha):
    delta = new_input - old_ema
    return old_ema + alpha * delta, (1 - alpha) * (old_var + alpha * delta ** 2)


def do_bbands(ma: Decimal, variance: Decimal):
    sd = variance.sqrt()
    return ma + 2 * sd, ma - 2 * sd


def do_rsi(avg_up, avg_down):
    return 100 - 100 / (1 + avg_up / avg_down)
