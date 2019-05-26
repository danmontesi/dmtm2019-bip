import pandas as pd

from datetime import timedelta

from tqdm import tqdm

CLUSTER_SIZE = 20000
DATASET = "bip_assignment/dataset_with_all_km.csv"


def preprocess():
    def categorizeData(data):
        time = data.hour
        if (time >= 6 and time <= 10):
            return "EarlyMorning"
        if (time >= 11 and time <= 14):
            return "LateMorning"
        if (time >= 15 and time <= 17):
            return "Afternoon"
        if (time >= 18 and time <= 21):
            return "Evening"
        if (time >= 22 and time <= 24):
            return "LateEvening"
        if (time >= 0 and time <= 5):
            return "Night"

    def add_column_basic(dataset):
        dataset['DISTANCE_FROM_POINT'] = dataset['KM'] - dataset['KM_START']
        dataset['LENGTH_KM'] = dataset['KM_END'] - dataset['KM_START']

        dataset['WEEK_DAY'] = dataset['DATETIME_UTC'].apply(lambda x: x.weekday())
        dataset['TIME_INTERVAL'] = dataset['DATETIME_UTC'].apply(categorizeData)

        dataset['DELTA_TIME_FROM_START'] = (dataset['DATETIME_UTC'] - dataset['START_DATETIME_UTC']).apply(lambda x: round(x.seconds/60, 1))

        road_df = pd.read_csv("bip_assignment/sensors.csv")

        dataset = dataset.join(road_df, lsuffix='', rsuffix='_sensor')

        return dataset

    def add_weather_stationid(dataset):
        weather_list=pd.DataFrame(columns=["KEY", "KM", "STATION_ID"])
        with open("bip_assignment/distances.csv") as f:
            for line in tqdm(f):
                splitted=line.split("|")
                chiavina=splitted[0].split(",")
                valorino=splitted[1].split(",")
                KEY=chiavina[0]
                KM=chiavina[1]
                STATION_ID=valorino[0]

                weather_list= weather_list.append({'KM': KM, 'KEY': KEY, 'STATION_ID': STATION_ID}, ignore_index=True)

        print(weather_list.head())

        dataset = dataset.join(weather_list, lsuffix='', rsuffix='_w')

        return dataset



    dataset = pd.read_csv("bip_assignment/dataset.csv")
    dataset['DATETIME_UTC'] = pd.to_datetime(dataset['DATETIME_UTC'])
    dataset['START_DATETIME_UTC'] = pd.to_datetime(dataset['START_DATETIME_UTC'])
    dataset['END_DATETIME_UTC'] = pd.to_datetime(dataset['END_DATETIME_UTC'])



    dataset = add_column_basic(dataset)


    dataset = add_weather_stationid(dataset)

    print(dataset.head())

    dataset.to_csv("bip_assignment/dataset_2.csv", index=False)


if __name__ == "__main__":
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_columns', 500)

    preprocess()