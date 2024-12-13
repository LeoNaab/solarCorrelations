import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

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


def calculate_variance(daily_data: pd.DataFrame):
    grouping = daily_data.groupby("state")
    variance = {}

    for state, group in grouping:
        variance[state] = group["GHI"].var()

    print("State Variances:", variance)
    return variance

def calculate_covariance_between_states(daily_data: pd.DataFrame):
    state_grouped = daily_data.groupby(["Year", "Month", "Day", "state"])["GHI"].mean().reset_index()
    pivoted_data = state_grouped.pivot(index=["Year", "Month", "Day"], columns="state", values="GHI")
    pivoted_data = pivoted_data.dropna()
    state_covariance = pivoted_data.cov()

    print("State Covariance Matrix:")
    print(state_covariance)

def plot_bivariate_distribution(daily_data: pd.DataFrame, state1: str, state2: str):
    data1 = daily_data[daily_data["state"] == state1].groupby(["Year", "Month", "Day"])["GHI"].mean().reset_index()
    data2 = daily_data[daily_data["state"] == state2].groupby(["Year", "Month", "Day"])["GHI"].mean().reset_index()

    merged_data = pd.merge(data1, data2, on=["Year", "Month", "Day"], suffixes=(f"_{state1}", f"_{state2}"))

    #Bivariate Distribution
    sns.scatterplot(x=f"GHI_{state1}", y=f"GHI_{state2}", data=merged_data, alpha=0.5, color="blue")
    plt.xlabel(f"GHI ({state1})")
    plt.ylabel(f"GHI ({state2})")
    plt.title(f"Bivariate Distribution of GHI: {state1} vs {state2}")
    plt.show()

    # Covariance between states
    covariance = merged_data[f"GHI_{state1}"].cov(merged_data[f"GHI_{state2}"])
    print(f"Covariance between {state1} and {state2}: {covariance}")


def seasonal_analysis(daily_data: pd.DataFrame):
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter (Dec, Jan, Feb)"
        elif month in [3, 4, 5]:
            return "Spring (Mar, Apr, May)"
        elif month in [6, 7, 8]:
            return "Summer (Jun, Jul, Aug)"
        else:
            return "Fall (Sept, Oct, Nov)"
    daily_data["Season"] = daily_data["Month"].apply(get_season)
    grouped_data = daily_data.groupby(["state", "Season"])["GHI"].mean()
    seasonal_avg = grouped_data.unstack()
    #print("Seasonal Averages for GHI by State:\n", seasonal_avg)
    seasonal_avg.T.plot(kind="bar", figsize=(10, 6))
    plt.title("Seasonal Average GHI by State")
    plt.xlabel("Season")
    plt.ylabel("Average GHI (Wh/m²)")
    plt.legend(title="State")
    plt.show()
    return seasonal_avg






# print(daily_data["GHI"])

if __name__ == "__main__":
    # Get and clean data
    daily_data: pd.DataFrame = pd.read_csv("/content/drive/MyDrive/SolarCorrections/daily_data/all-locations-daily.csv")
    daily_data = daily_data[daily_data["Year"] != 2002] # type: ignore

    hist_plot(daily_data)
    covariances, variances = calculate_variance(daily_data)
    calculate_covariance_between_states(daily_data)
    plot_bivariate_distribution(daily_data, "cal", "nm")
    seasonal_analysis(daily_data)