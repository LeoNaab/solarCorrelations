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


def hist_plot_all(daily_data):
    plt.hist(x=daily_data["GHI"], bins = 200)
    plt.title("California and New Mexico Daily GHI, 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("Occurrences")
    plt.show()

def hist_plot_each_state(daily_data):
    cal_data = state_daily_average(daily_data, "cal")
    nm_data = state_daily_average(daily_data, "nm")

    plt.subplot(1, 2, 1)
    plt.hist(x=cal_data["GHI"], bins = 200)
    plt.title("California (4 point average), 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("Occurrences")

    plt.subplot(1, 2, 2)
    plt.hist(x=nm_data["GHI"], bins = 200)
    plt.title("New Mexico (4 point average), 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("proportion of occurrences")

    plt.show()

def hist_plot_all_norm(daily_data):
    low = n_percent_low(daily_data, 1)["GHI"].max()

    plt.hist(x=daily_data["GHI"], bins = 200, density=True)
    plt.title("California and New Mexico Daily GHI, 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("proportion of occurrences")
    line = plt.axvline(low, c="red", ls="--", label=f"1% low: {low} W•h/m^2")
    plt.legend(handles=[line])

    plt.show()

def hist_plot_avg_norm(daily_data):
    grouped_data = interstate_daily_average(daily_data)

    low = n_percent_low(grouped_data, 1)["GHI"].max()

    plt.hist(x=grouped_data["GHI"], bins = 200, density=True)
    plt.title("8-Point Average Daily GHI, 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("proportion of occurrences")
    line = plt.axvline(low, c="red", ls="--", label=f"1% low: {low} W•h/m^2")
    plt.legend(handles=[line])

    plt.show()

def hist_plot_each_state_norm(daily_data):
    cal_data = state_daily_average(daily_data, "cal")
    nm_data = state_daily_average(daily_data, "nm")

    nm_low = n_percent_low(nm_data, 1)['GHI'].max()
    cal_low = n_percent_low(cal_data, 1)["GHI"].max()

    plt.subplot(1, 2, 1)
    plt.hist(x=cal_data["GHI"], bins = 200, density=True)
    plt.title("California (4 point average), 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("proportion of occurrences")
    line = plt.axvline(cal_low, c="red", ls="--", label=f"1% low: {cal_low} W•h/m^2")
    plt.legend(handles=[line])

    plt.subplot(1, 2, 2)
    plt.hist(x=nm_data["GHI"], bins = 200, density=True)
    plt.title("New Mexico (4 point average), 1998-2023")
    plt.xlabel("GHI (W•h/m^2)")
    plt.ylabel("proportion of occurrences")
    line = plt.axvline(nm_low, c="red", ls="--", label=f"1% low: {nm_low} W•h/m^2")
    plt.legend(handles=[line])

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


def calculate_variance_by_states(daily_data: pd.DataFrame):
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

def plot_statewise_distribution(daily_data: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="state", y="GHI", data=daily_data)
    plt.title("State-wise Distribution of GHI")
    plt.xlabel("State")
    plt.ylabel("GHI")
    plt.xticks(rotation=45)
    plt.show()

def one_percent(daily_data: pd.DataFrame):
    top_1_percent = daily_data.nlargest(int(0.01 * len(daily_data)), "GHI")
    bottom_1_percent = daily_data.nsmallest(int(0.01 * len(daily_data)), "GHI")
    print("Top 1% High GHI Days: ", top_1_percent)
    print("Bottom 1% Low GHI Days: ", bottom_1_percent)
    return top_1_percent, bottom_1_percent






# print(daily_data["GHI"])

if __name__ == "__main__":
    # Get and clean data
    # daily_data: pd.DataFrame = pd.read_csv("/content/drive/MyDrive/SolarCorrections/daily_data/all-locations-daily.csv")
    daily_data: pd.DataFrame = pd.read_csv("daily_data/all-locations-daily.csv")
    daily_data = daily_data[daily_data["Year"] != 2002] # type: ignore

    #Histogram of the plots
    hist_plot_all(daily_data)
    hist_plot_each_state(daily_data)
    hist_plot_all_norm(daily_data)
    hist_plot_each_state_norm(daily_data)
    hist_plot_avg_norm(daily_data)
    #Variance by state
    variances = calculate_variance_by_states(daily_data)
    #Covariance by state
    calculate_covariance_between_states(daily_data)
    #Bivariate plots
    plot_bivariate_distribution(daily_data, "cal", "nm")
    # Plotting GHI based off of seasons
    seasonal_analysis(daily_data)
    # Plotting the distribution based off of states
    plot_statewise_distribution(daily_data)
    #My attempt at a one_percent (bottom and top 1%)
    one_percent(daily_data)
