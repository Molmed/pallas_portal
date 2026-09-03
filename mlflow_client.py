import os
import pandas as pd
from dotenv import load_dotenv
import mlflow


class MlflowClient:
    def __init__(self):
        mlflow_env_path = os.path.join(os.path.dirname(__file__), "conf", "mlflow.env")
        load_dotenv(dotenv_path=mlflow_env_path)
        self.client = mlflow.tracking.MlflowClient()

    def get_registered_models(self):
        registered_models = self.client.search_registered_models()
        return [model.name for model in registered_models]

    def predict(self, model_name, df, error_tolerance):
        """
        Predict using the specified model and input data.
        :param model_name: Name of the registered model.
        :param input_data: Input data for prediction.
        :return: Predictions from the model.
        """
        model_uri = f"models:/{model_name}/latest"
        df = df.astype("float32")
        model = mlflow.pyfunc.load_model(model_uri)
        params = {'error_rate_alpha': error_tolerance / 100}
        predictions = model.predict(df, params=params)

        results = pd.Series(
            predictions,
            index=df.index,
            name="prediction",
            dtype=object,
        ).to_frame()

        return results

