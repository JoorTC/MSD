import numpy as np
import pandas as pd


class DataProcessor:

    def __init__(self, file_path, drop_column):
        self.filePath = file_path
        self.dropColumn = drop_column

    def load_and_preprocess_data(self):
        df = pd.read_csv(self.filePath, delimiter=',')
        df = df.iloc[0:, :]
        df.replace("NA", np.nan, inplace=True)
        y = df[self.dropColumn].astype(int)
        x = df.drop(columns=[self.dropColumn]).values
        return x, y

    def load_and_process_data(self):
        df = pd.read_csv(self.filePath, delimiter=',')
        df = df.iloc[0:, :]
        df.replace("NA", np.nan, inplace=True)
        return df
