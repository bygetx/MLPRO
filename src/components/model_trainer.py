import sys
import os
from dataclasses import dataclass

from sklearn.metrics import r2_score

from sklearn.ensemble import AdaBoostRegressor,RandomForestRegressor,GradientBoostingRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

from src.logger import logging
from src.exception import CustomException
from src.utils import save_object , evaluate_models
from src.params import params


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts" , "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self , train_arr , test_arr ):
        try:
            logging.info("splitting train test data")
            X_train , y_train , X_test , y_test = train_arr[:,:-1] , train_arr[:,-1],test_arr[:,:-1] , test_arr[:,-1]
            
            model = {
                "Random Forest" : RandomForestRegressor(),
                "Decision Tree" : DecisionTreeRegressor(),
                "Gradient Boosting" : GradientBoostingRegressor(),
                "Linear Regression" : LinearRegression(),
                "XGBRegressor" : XGBRegressor(),
                "CatBoosting Regressor" : CatBoostRegressor(verbose=False),
                "AdaBoost Regressor" : AdaBoostRegressor(),
            }

            model_report:dict = evaluate_models( X_train=X_train , y_train = y_train , X_test=X_test , y_test=y_test ,
                                                models = model , param=params)
            #get best model score
            best_model_score = max(sorted(list(model_report.values())))

            #get best model name
            """inverted_dict= {val:key for key , val in model_report.items()}
            best_model_name = inverted_dict[best_model_score]"""

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            best_model = model[best_model_name]

            if best_model_score< 0.6:
                raise CustomException("no best model found")
            
            logging.info(f"best model on test set was found to be {best_model_name}")

            save_object(file_path=self.model_trainer_config.trained_model_file_path,
                        obj=best_model)
            
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test , predicted)

            return r2_square


        except Exception as e:
            raise CustomException(e,sys)

