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

def average_files(paths: list[str]):
    assert (len(paths) > 0)

    frames = [pd.read_csv(path) for path in paths]

    # average = frames[]

def decode_location(filename: str):
    numbers: list[str] = []
    words: list[str] = []
    num = ""
    word = ""
    sign: str = ""

    for letter in filename:

        if letter.isdigit():
            num = num + letter
        elif len(num) > 0:
            numbers.append(num)
            num = ""

        if letter.isalpha():
            word = word + letter
        elif len(word) > 0:
            words.append(word)
            word = ""

    if words[1] == "n":
        sign = "-"
    else:
        sign = "+"

    return (words[0], numbers[0], sign + numbers[1])

def get_all_location_df(directory: str):

    file_list: list[str] = os.listdir(directory)
    for filename in file_list:
        assert(filename.count("-daily.csv") > 0)

    path: str = os.path.join(directory, file_list[0])



    concat_df: pd.DataFrame = pd.read_csv(path, index_col = 0)

    (state, lat, lon) = decode_location(file_list[0])
    concat_df["state"] = state
    concat_df["lat"] = lat
    concat_df["lon"] = lon

    for i in range(1, len(file_list)):
        path = os.path.join(directory, file_list[i])
        new_df = pd.read_csv(path, index_col = 0)

        (state, lat, lon) = decode_location(file_list[i])
        new_df["state"] = state
        new_df["lat"] = lat
        new_df["lon"] = lon


        concat_df = pd.concat([concat_df, new_df], ignore_index = True)


    print(concat_df)
    concat_df.to_csv('all-locations-daily.csv', index=False)



if __name__ == "__main__":
    # get_daily_sum("data", "nm35n104")
    # average_files([])
    get_all_location_df("daily_data")

    # print(decode_location("cal33n117-daily"))
