# ---
# jupyter:
#   jupytext:
#     cell_markers: region,endregion
#     formats: ipynb,.pct.py:percent,.lgt.py:light,.spx.py:sphinx,md,Rmd,.pandoc.md:pandoc,.myst.md:myst
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
"""
# A quick insight at world population

## Collecting population data

In the below we retrieve population data from the
[World Bank](http://www.worldbank.org/)
using the [wbdata](https://github.com/OliverSherouse/wbdata) python package
"""

# %%
import pandas as pd
import wbdata as wb

pd.options.display.max_rows = 6
pd.options.display.max_columns = 20

# %% [markdown]
# Corresponding indicator is found using search method - or, directly,
# the World Bank site.

# %%
wb.search_indicators('Population, total')  # SP.POP.TOTL
# wb.search_indicators('area')
# => https://data.worldbank.org/indicator is easier to use

# %% [markdown]
# Now we download the population data

# %%
indicators = {'SP.POP.TOTL': 'Population, total',
              'AG.SRF.TOTL.K2': 'Surface area (sq. km)',
              'AG.LND.TOTL.K2': 'Land area (sq. km)',
              'AG.LND.ARBL.ZS': 'Arable land (% of land area)'}
data = wb.get_dataframe(indicators, convert_date=True).sort_index()
data

# %% [markdown]
# World is one of the countries

# %%
data.loc['World']

# %% [markdown]
# Can we classify over continents?

# %%
data.loc[(slice(None), '2017-01-01'), :]['Population, total'].dropna(
).sort_values().tail(60).index.get_level_values('country')

# %% [markdown]
# Extract zones manually (in order of increasing population)

# %%
zones = ['North America', 'Middle East & North Africa',
         'Latin America & Caribbean', 'Europe & Central Asia',
         'Sub-Saharan Africa', 'South Asia',
         'East Asia & Pacific'][::-1]

# %% [markdown]
# And extract population information (and check total is right)

# %%
population = data.loc[zones]['Population, total'].swaplevel().unstack()
population = population[zones]
assert all(data.loc['World']['Population, total'] == population.sum(axis=1))

# %% [markdown]
# ## Stacked area plot with matplotlib

# %%
import matplotlib.pyplot as plt

# %%
plt.clf()
plt.figure(figsize=(10, 5), dpi=100)
plt.stackplot(population.index, population.values.T / 1e9)
plt.legend(population.columns, loc='upper left')
plt.ylabel('Population count (B)')
plt.show()

# %% [markdown]
# ## Stacked bar plot with plotly

# %%
import plotly.offline as offline
import plotly.graph_objs as go

offline.init_notebook_mode()

# %%
data = [go.Scatter(x=population.index, y=population[zone], name=zone, stackgroup='World')
        for zone in zones]
fig = go.Figure(data=data,
                layout=go.Layout(title='World population'))
offline.iplot(fig)
