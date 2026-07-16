import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}

    def preprocess_transaction(self, transaction_data: dict) -> np.ndarray:
        """
        Preprocess raw transaction data for ML models
        """
        df = pd.DataFrame([transaction_data])
        df = self.handle_missing_values(df)
        df = self.encode_categorical_features(df)
        return df.to_numpy()

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.fillna(0)

    def encode_categorical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.get_dummies(df)
