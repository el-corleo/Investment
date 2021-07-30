'''
Used to combine all individual datasets into one mega training set.
'''
import data_aggregator as da
import pandas as pd
import common

datasets_to_merge = []
for coin in common.coins:
	if coin != "polkadot":
		datasets_to_merge.append(pd.read_csv(f"datasets/complete/{coin}_historical_data_complete.csv"))

da.merge_datasets("all", datasets_to_merge, all_data=True)
