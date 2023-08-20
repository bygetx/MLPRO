import sys
import os
import numpy as np

from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler , OneHotEncoder

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from src.utils import save_object

@dataclass
class DataTransformationConfig():
    preprocessor_obj_file_path= os.path.join("artifacts" , "preprocessor.pkl")


class DataTransformation():
    def __init__(self) :
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):

        """
        function responsible for data transformation (both numerical and categorical) and returns the column transformer (preprocessor)
        """
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns =[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("num col standard scaling compleated")


            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("cat col encoding compleated")


            logging.info(f"categorical columns : {categorical_columns}")
            logging.info(f"numerical columns   : {numerical_columns}")


            preprocessor = ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    
    
    
    def initiate_data_transformation(self,train_path , test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("read train and test compleated")

            logging.info("obtaining preprocessor object")
            preprocessor_obj = self.get_data_transformer_object()

            target_column = "math_score"
            numerical_columns= ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column] , axis = 1)
            target_feature_train_df = train_df[target_column]
            input_feature_test_df = test_df.drop(columns=[target_column] , axis = 1)
            target_feature_test_df = test_df[target_column]

            logging.info(f"Applying preprocessing object on training and testing dataframe")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info("saving preprocessing object")
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,obj=preprocessor_obj)


            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path


            )





        except Exception as e:
            raise CustomException(e,sys)
