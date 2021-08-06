import pandas as pd
import numpy as np, numpy.random
import common
from typing import List, Tuple


VOLATILITY_TOLERANCE_THRESHOLD = 0.85
RETURN_TOLERANCE_THRESHOLD = 3

MAX_RETURN = 0
MIN_MAX_VOL_RET = 1
MAX_MIN_RET_VOL = 2
MIN_VOLATILITY = 3


def get_datasets(coins: List[str], interval: int) -> pd.DataFrame:
    portfolio_dataset = pd.DataFrame()
    for coin in coins:
        data = pd.read_csv(f"datasets/raw/{coin}_historical_data_raw.csv")
        data = data.iloc[:interval, :] # trim to specified interval

        start_date = data.iloc[0,0]
        end_date = data.iloc[data.shape[0]-1,0]

        data = data.drop(columns=["market_cap", "volume", "fear_greed"])
        data = common.handle_missing_data(data, start_date, end_date)
        data = data.iloc[::-1] # reverse dataset for later pct_change calculations

        portfolio_dataset[coin+"_price"] = data["price"]

    return portfolio_dataset



def calculate_portfolio_performance(weights: np.array, mean_returns: pd.DataFrame, covariance_matrix: pd.DataFrame, interval: int) -> Tuple[np.array, np.array]:
    returns = np.sum(mean_returns * weights) * interval
    std = np.sqrt(np.dot(weights.T, np.dot(covariance_matrix, weights))) * np.sqrt(interval)

    return returns, std



def print_results(coins: List[str], title: str, performance: Tuple[float, float], weights: np.array) -> None:
    print()
    print(title)
    print(f"Return: {performance[0]*100:.2f}% | Volatility: {performance[1]*100:.2f}%")
    report = ""
    for i in range(len(coins)):
        report += f"{coins[i]}: {weights[i]*100:.2f}% | "
    print(report)
    print()



def calculate_optimal_portfolio(coins: List[str], interval: int, n_simulations: int = 1000000) -> None:
    # load data
    portfolio_dataset = get_datasets(coins, interval)

    # get returns & covariance
    returns = portfolio_dataset.pct_change()
    mean_returns = returns.mean()
    covariance_matrix = returns.cov()

    # calculate portfolio performance
    best_performances = [(0,10), (0,10), (0,10), (0,10)] # (return, volatility)
    best_weights = [np.zeros(7), np.zeros(7), np.zeros(7), np.zeros(7)]
    for _ in range(n_simulations):
        # random weights whose sum = 1
        weights = np.random.dirichlet(np.ones(len(coins)), size=1)[0]
        performance = calculate_portfolio_performance(weights, mean_returns, covariance_matrix, interval)
        # Maximize returns
        if performance[0] > best_performances[MAX_RETURN][0]:
            best_performances[MAX_RETURN] = performance
            best_weights[MAX_RETURN] = weights
        # Minimize risk
        if performance[1] < best_performances[MIN_VOLATILITY][1]:
            best_performances[MIN_VOLATILITY] = performance
            best_weights[MIN_VOLATILITY] = weights
        # Maximize return for given risk
        if performance[0] > best_performances[MAX_MIN_RET_VOL][0] and performance[1] <= VOLATILITY_TOLERANCE_THRESHOLD:
            best_performances[MAX_MIN_RET_VOL] = performance
            best_weights[MAX_MIN_RET_VOL] = weights
        # Minimize risk for given return
        if performance[0] >= RETURN_TOLERANCE_THRESHOLD and performance[1] < best_performances[MIN_MAX_VOL_RET][1]:
            best_performances[MIN_MAX_VOL_RET] = performance
            best_weights[MIN_MAX_VOL_RET] = weights


    print_results(coins, "Max Return:", best_performances[MAX_RETURN], best_weights[MAX_RETURN])
    print_results(coins, "Min-Risk Given-Return:", best_performances[MIN_MAX_VOL_RET], best_weights[MIN_MAX_VOL_RET])
    print_results(coins, "Max-Return Given-Risk:", best_performances[MAX_MIN_RET_VOL], best_weights[MAX_MIN_RET_VOL])
    print_results(coins, "Min Risk:", best_performances[MIN_VOLATILITY], best_weights[MIN_VOLATILITY])

if __name__ == "__main__":
    coins = ["algorand", "bitcoin", "cardano", "ethereum", "solana"]
    calculate_optimal_portfolio(coins, 365, 1000000)