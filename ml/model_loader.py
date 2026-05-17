"""
Machine learning model loader.
"""

import warnings
import joblib
from pathlib import Path


class ModelLoader:
    """
    Load trained machine learning models
    and vectorizers from disk.
    """

    def __init__(self, model_path: str, vectorizer_path: str):

        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)

        self.model = None
        self.vectorizer = None

        self._load_models()

    def _load_models(self):
        """
        Load the trained model and vectorizer.
        """

        warnings.filterwarnings("ignore")

        try:
            print(f"[INFO] Loading model from: {self.model_path}")

            self.model = joblib.load(self.model_path)

            print(
                f"[INFO] Model loaded successfully "
                f"({type(self.model).__name__})"
            )

            print(
                f"[INFO] Loading vectorizer from: "
                f"{self.vectorizer_path}"
            )

            self.vectorizer = joblib.load(self.vectorizer_path)

            print(
                f"[INFO] Vectorizer loaded successfully "
                f"({type(self.vectorizer).__name__})"
            )

        except Exception as error:
            print(f"[ERROR] Failed to load model files: {error}")
            raise

    def get_model(self):
        """
        Return the loaded model.
        """

        if self.model is None:
            raise ValueError("Model is not loaded")

        return self.model

    def get_vectorizer(self):
        """
        Return the loaded vectorizer.
        """

        if self.vectorizer is None:
            raise ValueError("Vectorizer is not loaded")

        return self.vectorizer