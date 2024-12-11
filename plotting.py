import matplotlib.pyplot as plt
import pandas as pd




def hist_plot(daily_data):
    plt.hist(x=daily_data["GHI"], bins = 200)
    plt.show()


def average_days(daily_data: pd.DataFrame):
    grouped_data = daily_data.groupby(["Year", "Month", "Day"], as_index=False)["GHI"].mean()
    # hist_plot(grouped_data)
    # print(grouped_data)
    return grouped_data

# print(daily_data["GHI"])

if __name__ == "__main__":
    # Get and clean data
    daily_data: pd.DataFrame = pd.read_csv("daily_data/all-locations-daily.csv")
    daily_data = daily_data[daily_data["Year"] != 2002] # type: ignore

    # hist_plot(daily_data)
    # average_days(daily_data)
    hist_plot(average_days(daily_data))
