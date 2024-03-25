liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

FEE = 0.003


def get_reserves(tokenA, tokenB):
    """
    Implement a function to get the reserves of a pair of tokens.
    """
    if (tokenA, tokenB) in liquidity:
        return liquidity[(tokenA, tokenB)]
    elif (tokenB, tokenA) in liquidity:
        return liquidity[(tokenB, tokenA)][::-1]
    else:
        return None


def get_amount_out(amount_in, reserve_in, reserve_out):
    """
    Implement a function to calculate the amount of output token given an input amount.
    """
    amount_in_with_fee = amount_in * (1 - FEE)
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in + amount_in_with_fee
    amount_out = numerator / denominator
    return amount_out


def get_amounts_out(amount_in, path):
    """
    Implement a function to calculate the amount of output token given an input amount and a path.
    """
    amounts = [amount_in]
    for i in range(len(path) - 1):
        reserve_in, reserve_out = get_reserves(path[i], path[i + 1])
        amount_in = amounts[-1]
        amount_out = get_amount_out(amount_in, reserve_in, reserve_out)
        # if amount_out * amount_in * (1 - FEE) ** 2 < reserve_in * reserve_out:
        #     amounts.append(0)
        # else:
        amounts.append(amount_out)
    return amounts


def find_arbitrage_path(
    liquidity, path=[], max_depth=5, best_path=None, best_balance=0
):
    """
    Using DFS algorithm to find a profitable path.
    """
    # print(f"current path: {path}, best path: {best_path}, best balance: {best_balance}")
    if len(path) > max_depth:
        return best_path, best_balance

    if len(path) > 1:
        final_balance = get_amounts_out(5, path)[-1]
        if final_balance > best_balance and path[-1] == "tokenB":
            best_balance = final_balance
            best_path = path

    for token in ["tokenA", "tokenB", "tokenC", "tokenD", "tokenE"]:
        if token != path[-1]:
            new_path = path + [token]
            best_path, best_balance = find_arbitrage_path(
                liquidity, new_path, max_depth, best_path, best_balance
            )

    return best_path, best_balance


if __name__ == "__main__":
    # find_arbitrage_path(liquidity)
    best_path, best_balance = find_arbitrage_path(
        liquidity, path=["tokenB"], max_depth=5
    )
    final_balance = get_amounts_out(5, best_path)
    print(f"path: {'->'.join(best_path)}, tokenB balance={final_balance[-1]:.6f}.")
