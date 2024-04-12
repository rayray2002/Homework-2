# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1

Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

> Solution
>
> Path: `tokenB->tokenA->tokenD->tokenC->tokenB`
>
> 1. `tokenB->tokenA`: amountIn: 5, amountOut: 5.655321988655323
> 2. `tokenA->tokenD`: amountIn: 5.655321988655323, amountOut: 2.458781317097934
> 3. `tokenD->tokenC`: amountIn: 2.458781317097934, amountOut: 5.0889272933015155
> 4. `tokenC->tokenB`: amountIn: 5.0889272933015155, amountOut: 20.129888944077447

## Problem 2

What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

> Solution
>
> Slippage refers to the difference between the expected price of a trade and the actual price. This problem can occur due to the time lag between when a transaction is submitted and when it is confirmed on the blockchain, during which the price can change because of other trades being executed.
>
> Uniswap V2 allows user to set a tolerance for the price difference. If the actual price of the trade at execution time is worse than this tolerance, the transaction will revert and fail, protecting the user from slippage.
>
> We can refer to [UniswapV2Router02.sol](https://github.com/Uniswap/v2-periphery/blob/0335e8f7e1bd1e8d8329fd300aea2ef2f36dd19f/contracts/UniswapV2Router02.sol#L246) line 246 swapTokensForExactTokens. We can set amountInMax and the function will revert if the actual amountIn is greater than the amountInMax.

```solidity
function swapTokensForExactTokens(
    uint amountOut,
    uint amountInMax,
    address[] calldata path,
    address to,
    uint deadline
) external virtual override ensure(deadline) returns (uint[] memory amounts) {
    amounts = UniswapV2Library.getAmountsIn(factory, amountOut, path);
    require(amounts[0] <= amountInMax, 'UniswapV2Router: EXCESSIVE_INPUT_AMOUNT');
    TransferHelper.safeTransferFrom(
        path[0], msg.sender, UniswapV2Library.pairFor(factory, path[0], path[1]), amounts[0]
    );
    _swap(amounts, path, to);
}
```

## Problem 3

Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

> Solution
>
> When the first liquidity provider supplies liquidity to a new pool, a certain amount of liquidity tokens, known as "minimum liquidity," is permanently locked in the pool (`liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY)`). This is done by minting the minimum liquidity amount and sending it to the zero address. The rationale behind this design is to avoid issues with rounding errors and to prevent someone from owning an entire pool with a very small initial investment.

## Problem 4

Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

> Solution
>
> The minting function in the UniswapV2Pair contract uses a specific formula (min of two ratio: `liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1)`) to determine the amount of liquidity tokens that a liquidity provider receives when depositing tokens into the pool. This formula is designed to maintain the ratio of the liquidity provider's share in the pool relative to the total liquidity.

```solidity
function mint(address to) external lock returns (uint liquidity) {
    (uint112 _reserve0, uint112 _reserve1,) = getReserves(); // gas savings
    uint balance0 = IERC20(token0).balanceOf(address(this));
    uint balance1 = IERC20(token1).balanceOf(address(this));
    uint amount0 = balance0.sub(_reserve0);
    uint amount1 = balance1.sub(_reserve1);

    bool feeOn = _mintFee(_reserve0, _reserve1);
    uint _totalSupply = totalSupply; // gas savings, must be defined here since totalSupply can update in _mintFee
    if (_totalSupply == 0) {
        liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
        _mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the first MINIMUM_LIQUIDITY tokens
    } else {
        liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
    }
    require(liquidity > 0, 'UniswapV2: INSUFFICIENT_LIQUIDITY_MINTED');
    _mint(to, liquidity);

    _update(balance0, balance1, _reserve0, _reserve1);
    if (feeOn) kLast = uint(reserve0).mul(reserve1); // reserve0 and reserve1 are up-to-date
    emit Mint(msg.sender, amount0, amount1);
}
```

## Problem 5

What is a sandwich attack, and how might it impact you when initiating a swap?

> Solution
>
> A sandwich attack is a malicious actor spots a pending transaction on a DEX that will affect the price of an asset. The attacker then places a buy order before the detected transaction, and a sell order right after, benefiting from the price slippage caused by the victim's transaction. This can lead to the victim receiving a worse price for their swap due to the attacker's manipulation.
