"""
CyberGuard AML Multi-Model Ensemble Classifier
Implements the 5 required research architectures:
1. Support Vector Machine (Calibrated SGDClassifier with modified Huber loss)
2. XGBoost (Extreme Gradient Boosted Trees)
3. LightGBM (Lightweight Gradient Boosted Trees)
4. CatBoost (Categorical Boosting)
5. CyberGuard Stacking Ensemble (Meta-Learner: Calibrated Logistic Regression)
"""
import os
import time
import json
import joblib
import numpy as np
from pathlib import Path
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import lightgbm as lgb
import catboost as cb
from sklearn.model_selection import StratifiedKFold, cross_val_predict

UNIFIED_CLASSES = [
    "Age-based",
    "Gender-based",
    "Religion-based",
    "Ethnicity-based",
    "Appearance-based",
    "Mockery/Defamation",
    "Abusive/Insult",
    "Threat/Intimidation",
    "Personal Harassment",
    "Non-cyberbullying"
]

class CyberbullyingAMLClassifier:
    """
    AML Multi-Model Framework:
    Fits and compares SVM, XGBoost, LightGBM, CatBoost, and Stacking Ensemble.
    """

    def __init__(self, classes: list = None):
        self.classes = sorted(classes or UNIFIED_CLASSES)
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.classes)

        # 1. Calibrated SVM
        self.svm_model = CalibratedClassifierCV(
            estimator=SGDClassifier(loss="modified_huber", alpha=1e-4, max_iter=2000, random_state=42),
            cv=3
        )
        # 2. XGBoost
        self.xgb_model = xgb.XGBClassifier(
            n_estimators=60,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
            n_jobs=4,
            eval_metric="mlogloss"
        )
        # 3. LightGBM
        self.lgb_model = lgb.LGBMClassifier(
            n_estimators=60,
            max_depth=5,
            learning_rate=0.1,
            num_leaves=31,
            random_state=42,
            n_jobs=4,
            verbose=-1
        )
        # 4. CatBoost
        self.cb_model = cb.CatBoostClassifier(
            iterations=60,
            depth=5,
            learning_rate=0.1,
            random_seed=42,
            thread_count=4,
            verbose=0
        )
        # 5. Stacking Meta-Learner weights / blender
        self.meta_learner = LogisticRegression(max_iter=500, random_state=42)

        self.is_fitted = False
        self.training_times = {}

    def fit(self, X: np.ndarray, y: list):
        y_array = np.asarray(y)
        cleaned_labels = np.asarray([
            label if label in self.classes else "Non-cyberbullying"
            for label in y_array
        ])
        encoded_labels = self.label_encoder.transform(cleaned_labels)

        _, class_counts = np.unique(encoded_labels, return_counts=True)
        if len(class_counts) != len(self.classes) or class_counts.min() < 5:
            raise ValueError("Five-fold stacking requires at least 5 examples of every class.")

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        base_models = [
            ("svm", self.svm_model, cleaned_labels),
            ("xgboost", self.xgb_model, encoded_labels),
            ("lightgbm", self.lgb_model, encoded_labels),
            ("catboost", self.cb_model, encoded_labels),
        ]

        stacking_started = time.time()
        meta_features = []

        for model_name, model, targets in base_models:
            model_started = time.time()
            oof_probs = cross_val_predict(
                model,
                X,
                targets,
                cv=cv,
                method="predict_proba",
                n_jobs=1,
            )
            if oof_probs.shape[1] != len(self.classes):
                raise ValueError(f"{model_name} returned an unexpected class order/shape.")

            meta_features.append(oof_probs)
            model.fit(X, targets)
            self.training_times[model_name] = time.time() - model_started

        meta_X = np.hstack(meta_features)
        self.meta_learner.fit(meta_X, encoded_labels)
        self.training_times["stacking"] = time.time() - stacking_started

        self.is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray, model_type: str = "stacking") -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Classifier has not been fitted or loaded yet.")

        if X.ndim == 1:
            X = X.reshape(1, -1)

        if model_type == "svm":
            # Map svm_model classes to canonical class order
            raw_p = self.svm_model.predict_proba(X)
            # Reorder columns to match self.classes
            svm_classes = list(self.svm_model.classes_)
            ordered_p = np.zeros((X.shape[0], len(self.classes)), dtype=np.float32)
            for i, cls in enumerate(self.classes):
                if cls in svm_classes:
                    idx = svm_classes.index(cls)
                    ordered_p[:, i] = raw_p[:, idx]
            probs = ordered_p
        elif model_type == "xgboost":
            probs = self.xgb_model.predict_proba(X)
        elif model_type == "lightgbm":
            probs = self.lgb_model.predict_proba(X)
        elif model_type == "catboost":
            probs = self.cb_model.predict_proba(X)
        else: # stacking
            p_svm = self.predict_proba(X, model_type="svm")
            p_xgb = self.xgb_model.predict_proba(X)
            p_lgb = self.lgb_model.predict_proba(X)
            p_cb = self.cb_model.predict_proba(X)
            meta_X = np.hstack([p_svm, p_xgb, p_lgb, p_cb])
            probs = self.meta_learner.predict_proba(meta_X)

        # Normalize probability rows safely
        row_sums = probs.sum(axis=1, keepdims=True)
        return (probs / np.maximum(row_sums, 1e-9)).astype(np.float32)

    def predict(self, X: np.ndarray, model_type: str = "stacking") -> tuple:
        probs = self.predict_proba(X, model_type=model_type)
        pred_indices = np.argmax(probs, axis=1)
        confidences = np.max(probs, axis=1)
        labels = [self.classes[idx] for idx in pred_indices]
        return labels, confidences

    def save(self, model_dir: str):
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        artifacts = {
            "svm_model": self.svm_model,
            "xgb_model": self.xgb_model,
            "lgb_model": self.lgb_model,
            "cb_model": self.cb_model,
            "meta_learner": self.meta_learner,
            "label_encoder": self.label_encoder,
            "classes": self.classes,
            "training_times": self.training_times
        }
        joblib.dump(artifacts, os.path.join(model_dir, "classifier_models.joblib"))
        with open(os.path.join(model_dir, "classes.json"), "w") as f:
            json.dump(self.classes, f, indent=2)

    def load(self, model_dir: str):
        path = os.path.join(model_dir, "classifier_models.joblib")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Classifier artifacts not found at {path}")
        artifacts = joblib.load(path)
        self.svm_model = artifacts["svm_model"]
        self.xgb_model = artifacts["xgb_model"]
        self.lgb_model = artifacts["lgb_model"]
        self.cb_model = artifacts["cb_model"]
        self.meta_learner = artifacts["meta_learner"]
        self.label_encoder = artifacts["label_encoder"]
        self.classes = artifacts["classes"]
        self.training_times = artifacts.get("training_times", {})
        self.is_fitted = True
        return self
