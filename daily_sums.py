import pandas as pd
import os


def get_daily_sum(directory: str, subdirectory: str):
    """Takes directory and folder name of raw NSRDB hourly data, and sums the results of all files
    into a single file with daily GHI and DNI sums
    """
    file_list: list[str] = os.listdir(os.path.join(directory,subdirectory))

    path: str = os.path.join(directory, subdirectory, file_list[0])

    sum_df: pd.DataFrame = pd.read_csv(path, skiprows=[0,1])

    for i in range(1, len(file_list)):
        path = os.path.join(directory, subdirectory, file_list[i])
        sum_df = pd.concat([sum_df, pd.read_csv(path, skiprows=[0,1])], ignore_index = True)


    sum_df1 = sum_df.groupby(["Year", "Month", "Day"], as_index=False).sum("GHI") # type: ignore
    sum_df2 = sum_df1[["Year", "Month", "Day", "GHI", "DNI"]]
    sum_df2.to_csv(f'{subdirectory}-daily.csv')
    print(sum_df2)

if __name__ == "__main__":
    get_daily_sum("data", "nm35n104")
