import os
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

        # Print model names
        for model in registered_models:
            print(model.name)


# import mlflow.sklearn


# model = mlflow.sklearn.load_model("models:/my_model/Production")
# predictions = model.predict(input_data)
