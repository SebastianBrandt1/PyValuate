import pandas as pd
import os
import pandas_datareader
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import quandl

api_key = "EzveDSFN9V7T3JGstQ_M"
pickle_file = "../Data/us_states.pkl"


def get_us_state_list():
    us_states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
    return us_states[0][0][1:]


def get_initial_state_data(file=pickle_file):
    us_states = get_us_state_list()
    main_df = pd.DataFrame()
    for state in us_states:
        df = quandl.get("FMAC/HPI_{}".format(state), authtoken=api_key)
        df["Value"] = (df["Value"] - df["Value"][0])/df["Value"][0] * 100.0
        df.rename(columns={"Value": "{}_HPI".format(state)}, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how="outer")

    main_df.to_pickle(file)
    return main_df


def get_us_benchmark_HPI():
    if os.path.exists("../Data/us_hpi_benchmark.pkl"):
        print("Local Benchmark")
        return pd.read_pickle("../Data/us_hpi_benchmark.pkl")
    else:
        print("Web Benchmark")
        df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
        df["Value"] = (df["Value"] - df["Value"][0]) / df["Value"][0] * 100.0
        df.rename(columns={"Value": "HPI_USA"}, inplace=True)
        #df.set_index(["Date"], inplace=True)
        df.to_pickle("../Data/us_hpi_benchmark.pkl")
        return df


def get_states_from_picke(filename):
    return pd.read_pickle(filename)


def plot_data(df, benchmark):
    style.use("fivethirtyeight")
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    df.plot(ax=ax1)
    benchmark.plot(ax=ax1, color="k", linewidth=10)

    plt.legend().remove()
    plt.show()


if os.path.exists(pickle_file):
    print("Local data")
    HPI_data = get_states_from_picke(pickle_file)
else:
    print("Web data")
    HPI_data = get_initial_state_data()

benchmark = get_us_benchmark_HPI()
#plot_data(HPI_data, benchmark)

HPI_TX_1Y = HPI_data["TX_HPI"].resample("A").sum()
HPI_TX_1Y.plot()
HPI_data["TX_HPI"].plot()
plt.show()
index_date = "2016-02-29"
# to_date = datetime(index_date) - datetime.timedelta(days=7)
#print(benchmark.loc[index_date:"2015-07-31":-1])

#HPI_correlation = HPI_data.corr()
#print(HPI_correlation.describe())

# #df = quandl.get("FMAC/HPI_AK", authtoken=api_key)
# #
# # #print(df.head())
# #
# fifty_states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
# #
# # print(fifty_states[0][0][1:])
# for abbv in fifty_states[0][0][1:]:
#      print("FMAC/HPI_{}".format(abbv))
#
#
# df1 = pd.DataFrame({'HPI':[80,85,88,85],
#                     'Int_rate':[2, 3, 2, 2],
#                     'US_GDP_Thousands':[50, 55, 65, 55]},
#                    index = [2001, 2002, 2003, 2004])
#
# df2 = pd.DataFrame({'HPI':[80,85,88,85],
#                     'Int_rate':[2, 3, 2, 2],
#                     'US_GDP_Thousands':[50, 55, 65, 55]},
#                    index = [2005, 2006, 2007, 2008])
#
# df3 = pd.DataFrame({'HPI':[80,85,88,85],
#                     'Unemployment':[7, 8, 9, 6],
#                     'Low_tier_HPI':[50, 52, 50, 53]},
#                    index = [2001, 2002, 2003, 2004])
#
# df1.set_index("HPI", inplace=True)
# df3.set_index("HPI", inplace=True)
#
# df4 = df1.join(df3)
# print(df4)
# # print(pd.merge(df1,df3, on='HPI'))
# # df4 = pd.merge(df1, df2, on="HPI")
# # df4.fillna(0, inplace=True)
# # print(df4)


# style.use("ggplot")
#
# web_stats = {"Day": [1, 2, 3, 4, 5, 6],
#              "Visitors": [43, 22, 64, 234, 543, 213],
#              "Bounce_Rate": [4, 41, 213, 532, 213, 123]}
#
# df = pd.DataFrame(web_stats)
# df.set_index("Day", inplace=True)
#
# arr = np.array(df[["Visitors", "Bounce_Rate"]])
# print(arr[1][1])
#
#
# df_csv = pd.read_csv("../Data/ZILL-Z77006_A.csv")
# df_csv.set_index("Date", inplace=True)
# df_csv.to_csv("../Data/new_housing.csv")
#
# df = pd.read_csv("../Data/new_housing.csv", index_col=0)
# df.columns = ["Austin_HPI"]
# df.to_csv("../Data/new_housing_no_head.csv", header=False)
#
# df = pd.read_csv("../Data/new_housing_no_head.csv", names=["Date", "Austin_HPI"], index_col=0)

# df = pd.read_csv("../Data/new_housing.csv", index_col="Date")
# df.rename(columns={"Value": "Austin_HPI_new"}, inplace=True)

# print(df.loc[["1996-04-30", "1997-01-31"]])

# startdate = datetime.date(2001, 1, 1)
# endtime = datetime.date(2016. 12. 31)

# df = web.Datareader()


