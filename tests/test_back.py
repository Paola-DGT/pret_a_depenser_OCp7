import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from app import ml_tools


class TestMlTools:
    def test_train_and_predict(self):
        data_from_front = {
            "FLAG_OWN_CAR": 0,
            "FLAG_OWN_REALTY": 0,
            "CNT_CHILDREN": 0,
            "AMT_INCOME_TOTAL": 1,
            "AMT_CREDIT": 1,
            "EXT_SOURCE_1": 0.5059,
            "DAYS_BIRTH": -7018,
            "ANNUITY_INCOME_PERC": 1,
            "DAYS_EMPLOYED_PERC": 19.22739726027397,
            "INCOME_CREDIT_PERC": 1,
            "PAYMENT_RATE": 1,
            "AMT_ANNUITY": 1,
        }

        from app.prediction_server import FormRequest

        data = FormRequest(**data_from_front)

        model = ml_tools.train_and_return()
        predict_proba = model.predict_proba(pd.DataFrame(data.dict(), index=[0]))
        predict = model.predict(pd.DataFrame(data.dict(), index=[0]))
        assert isinstance(model, RandomForestClassifier)
        assert (predict_proba == [0.6, 0.4]).all()
        assert predict[0] == 0