import argparse

import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.power import FTestAnovaPower


parser = argparse.ArgumentParser(description='Power Analysis Script.')
parser.add_argument("--alpha", type=float, default=0.05)
parser.add_argument("--power", type=float, default=0.8)
parser.add_argument("--dataset", default="rcdv")
parser.add_argument("--metric", default="accuracy")
parser.add_argument("--data_file", default="database.jsonl")

args = parser.parse_args()


df_all = pd.read_json(args.data_file, lines=True)

alpha = args.alpha
power = args.power
dataset = args.dataset
metric = args.metric

df = df_all[df_all['condition'].str.startswith(dataset)]
model = ols(f'{metric} ~ C(condition)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table['sum_sq'])
n_groups = df['condition'].nunique()

SSB = anova_table['sum_sq'][0]
SST = anova_table['sum_sq'].sum()
eta_squared = SSB / SST

ft = FTestAnovaPower()
sample_size = ft.solve_power(
    effect_size=eta_squared, nobs=None, alpha=alpha, power=power, 
    k_groups=n_groups)
print(f"Required sample size for {dataset}: {round(sample_size)}")
