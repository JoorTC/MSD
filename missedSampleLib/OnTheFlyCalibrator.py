import numpy as np


def _clip01(p, eps=1e-6):
    return np.clip(p, eps, 1 - eps)


def _logit(p):
    p = _clip01(p)
    return np.log(p / (1 - p))


def _sigmoid(z):
    return 1 / (1 + np.exp(-z))


class OnTheFlyCalibrator:

    def __init__(self, base_model, pi_train, a=0.0, b=1.0, clip=1e-6, default_pi_target=None):
        self.base_model = base_model
        self.pi_train = float(pi_train)
        self.a = float(a)
        self.b = float(b)
        self.clip = float(clip)
        self.default_pi_target = default_pi_target

    def _prior_offset(self, pi_target):
        return _logit(_clip01(pi_target, self.clip)) - _logit(_clip01(self.pi_train, self.clip))

    def _ensure_2d(self, X):
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        return X

    def predict_proba(self, X, pi_target=None):
        X = self._ensure_2d(X)

        # 1) proba cruda del modelo
        p_raw = self.base_model.predict_proba(X)[:, 1]
        p_raw = _clip01(p_raw, self.clip)
        z = _logit(p_raw)

        z = self.a + self.b * z

        if pi_target is None:
            pi_target = self.default_pi_target
        if pi_target is not None:
            z = z + self._prior_offset(float(pi_target))

        p_cal = _sigmoid(z)
        return np.column_stack([1 - p_cal, p_cal])
        # return np.vstack([1 - p_cal, p_cal]).T

    def predict(self, X, threshold=0.5, pi_target=None):
        # X_new = np.asarray(X, dtype=float).reshape(1, -1)
        # proba = self.predict_proba(X_new, pi_target=pi_target)[:, 1]
        proba = self.predict_proba(X, pi_target=pi_target)[:, 1]
        return (proba >= float(threshold)).astype(int)

    def set_calibration(self, a, b):
        self.a = float(a)
        self.b = float(b)

    def set_training_prevalence(self, pi_train):
        self.pi_train = float(pi_train)

    def set_default_target_prevalence(self, pi_target):
        self.default_pi_target = float(pi_target)
