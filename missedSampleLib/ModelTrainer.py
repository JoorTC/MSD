import numpy as np
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from xgboost import XGBClassifier
import missedSampleLib.utils
from missedSampleLib import DataProcessor
from missedSampleLib import OnTheFlyCalibrator


class ModelTrainer:

    def __init__(self):
        self.dp = DataProcessor('../missedSampleLib-base/missedSampleLib/train_set.csv', 'Error_ID')
        self.xTrain, self.yTrain = self.dp.load_and_preprocess_data()
        self.wrapped_model = None
        self.best_model = None
        self.feature_order = self.dp.get_feature_order() if hasattr(self.dp, "get_feature_order") else None

    def train_model(self, default_pi_target=0.05):
        kFold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        xgb = XGBClassifier(
            eval_metric="auc",
            random_state=42,
            missing=np.nan
        )

        grid_search = GridSearchCV(
            estimator=xgb,
            param_grid=missedSampleLib.utils.get_param_grid(),
            scoring="roc_auc",
            cv=kFold,
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(self.xTrain, self.yTrain)

        self.best_model = grid_search.best_estimator_

        pi_train = float(np.mean(self.yTrain))
        DEFAULT_PI_TARGET = 0.05
        CALIB_A = 0.0
        CALIB_B = 1.0

        self.wrapped_model = missedSampleLib.OnTheFlyCalibrator(self.best_model, pi_train, a=CALIB_A, b=CALIB_B, default_pi_target=DEFAULT_PI_TARGET)

        return {
            "best_params_": grid_search.best_params_,
            "cv_best_auc": grid_search.best_score_,
            "pi_train": pi_train,
            "calib_a": CALIB_A,
            "calib_b": CALIB_B,
            "default_pi_target": default_pi_target
        }

    def evaluate_model(self, model, x_test, pi_target=None, return_proba=True, threshold=0.5):
        if isinstance(model, OnTheFlyCalibrator):
            if return_proba:
                return model.predict_proba(x_test, pi_target=pi_target)[:, 1]
            else:
                return model.predict(x_test, threshold=threshold, pi_target=pi_target)
        else:
            # modelo crudo (XGB): sin prior shift ni calibración
            if return_proba:
                return model.predict_proba(x_test)[:, 1]
            else:
                p = model.predict_proba(x_test)[:, 1]
                return (p >= float(threshold)).astype(int)
