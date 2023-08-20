from src.exception import CustomException
import sys
import os
import dill
import numpy as np
import pandas as pd


def save_object(file_path , obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path , exist_ok=True)
        with open(file_path, "wb") as file:
            dill.dump(obj,file)
    except Exception as e:
        raise CustomException(e,sys)