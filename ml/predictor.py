"""
Sentiment prediction module.
"""

from typing import Dict, List, Union

import numpy as np

from utils.preprocessing import clean_text


class Predictor:
    """
    Handles sentiment prediction using a trained ML model.
    """

    def __init__(self, model, vectorizer):

        self.model = model
        self.vectorizer = vectorizer

        # Numeric label mapping
        self.label_mapping = {
            0: "Negative",
            1: "Neutral",
            2: "Positive"
        }

    # =========================================================
    # Single Prediction
    # =========================================================

    def predict(self, text: str) -> Dict[str, Union[str, float]]:
        """
        Predict sentiment for a single text.
        """

        # Clean input text
        cleaned_text = clean_text(text)

        # Handle empty input
        if not cleaned_text:
            return {
                "sentiment": "Neutral",
                "confidence": 0.0
            }

        try:
            # Convert text into numerical features
            X = self.vectorizer.transform([cleaned_text])

            # Run prediction
            prediction = self.model.predict(X)[0]

            # Convert numeric labels into readable labels
            if isinstance(prediction, (int, np.integer)):
                sentiment = self.label_mapping.get(
                    int(prediction),
                    "Neutral"
                )
            else:
                sentiment = str(prediction)

            # Calculate confidence score
            confidence = self._calculate_confidence(X)

            return {
                "sentiment": sentiment,
                "confidence": round(confidence, 3)
            }

        except Exception as e:

            print(f"[ERROR] Prediction failed: {e}")

            return {
                "sentiment": "Neutral",
                "confidence": 0.0
            }

    # =========================================================
    # Batch Prediction
    # =========================================================

    def predict_batch(self, texts: List[str]) -> List[Dict]:
        """
        Predict sentiment for multiple texts.
        """

        # Clean all texts
        cleaned_texts = [
            clean_text(text) if text else ""
            for text in texts
        ]

        try:
            # Vectorize texts
            X = self.vectorizer.transform(cleaned_texts)

            # Run predictions
            predictions = self.model.predict(X)

            results = []

            for i, prediction in enumerate(predictions):

                # Convert labels
                if isinstance(prediction, (int, np.integer)):
                    sentiment = self.label_mapping.get(
                        int(prediction),
                        "Neutral"
                    )
                else:
                    sentiment = str(prediction)

                # Confidence score
                confidence = self._calculate_confidence(X[i])

                results.append({
                    "sentiment": sentiment,
                    "confidence": round(confidence, 3)
                })

            return results

        except Exception as e:

            print(f"[ERROR] Batch prediction failed: {e}")

            # Return default predictions
            return [
                {
                    "sentiment": "Neutral",
                    "confidence": 0.0
                }
                for _ in texts
            ]

    # =========================================================
    # Confidence Calculation
    # =========================================================

    def _calculate_confidence(self, X) -> float:
        """
        Calculate prediction confidence score.
        """

        confidence = 1.0

        # Models supporting probability prediction
        if hasattr(self.model, "predict_proba"):

            probabilities = self.model.predict_proba(X)[0]

            confidence = float(np.max(probabilities))

        # Models supporting decision function
        elif hasattr(self.model, "decision_function"):

            decision = self.model.decision_function(X)[0]

            if isinstance(decision, np.ndarray):
                confidence = float(np.max(np.abs(decision)))
            else:
                confidence = float(abs(decision))

            # Normalize score between 0 and 1
            confidence = min(1.0, max(0.0, confidence / 10))

        return confidence