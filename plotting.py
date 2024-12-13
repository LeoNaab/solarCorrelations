import matplotlib.pyplot as plt
import pandas as pd


# Data ideas
# 1% low (state vs interstate)
# covariance (between state points vs interstate)
# correlation coefficient
# variance (state vs interstate)

# per month data
# covariance (between state points vs interstate)
# correlation coefficient
# variance (state vs interstate)


def hist_plot(daily_data):
    plt.hist(x=daily_data["GHI"], bins = 200)
    plt.xlabel("GHI (W•h/m^2")
    plt.ylabel("Occurances")
    plt.show()


def state_daily_average(daily_data: pd.DataFrame, state: str):
    grouped_data = daily_data[daily_data["state"] == state]
    grouped_data = grouped_data.groupby(["Year", "Month", "Day", ], as_index=False)["GHI"].mean()
    # hist_plot(grouped_data)
    # print(grouped_data)
    return grouped_data

def interstate_daily_average(daily_data: pd.DataFrame):
    grouped_data = daily_data.groupby(["Year", "Month", "Day"], as_index=False)["GHI"].mean()
    # hist_plot(grouped_data)
    # print(grouped_data)
    return grouped_data

def n_percent_low(daily_data: pd.DataFrame, percentage):
    """
    Takes in a Dataframe with daily GHI data and returns the lowest {percentage} percent of the rows
    """
    low_days = len(daily_data) * percentage//100

    out_frame = daily_data.nsmallest(low_days, "GHI")

    return out_frame


# print(daily_data["GHI"])

if __name__ == "__main__":
    # Get and clean data
    daily_data: pd.DataFrame = pd.read_csv("daily_data/all-locations-daily.csv")
    daily_data = daily_data[daily_data["Year"] != 2002] # type: ignore

    hist_plot(daily_data)

    # average_days(daily_data)
    # print(n_percent_low(daily_data, 1)["GHI"].max())
    # print(n_percent_low(state_daily_average(daily_data, "cal"), 1)["GHI"].max()) #type: ignore
    # print(n_percent_low(interstate_daily_average(daily_data), 1)["GHI"].max()) #type: ignore
    # hist_plot(interstate_daily_average(daily_data))

    # print(state_daily_average(daily_data, "cal"))
    # hist_plot(state_daily_average(daily_data, "cal"))
