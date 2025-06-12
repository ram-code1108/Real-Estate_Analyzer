import pickle 
import json
import numpy as np
import pandas as pd 
__locations=None
__data_columns=None
__model=None


def get_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location) 
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[__data_columns.index("total_sqft")] = sqft  
    x[__data_columns.index("bath")] = bath
    x[__data_columns.index("bhk")] = bhk  

    if loc_index >= 0:
        x[loc_index] = 1

    x_df = pd.DataFrame([x], columns=__data_columns)

    return round(__model.predict(x_df)[0], 2)










def load_artifacts():
    print("Loading saved artfacts")
    global __data_columns
    global __locations
    
    with open(r"D:\RKT\Python files\my projects\bang_lore_final_final\columns_linear.json","r") as f:
        __data_columns=json.load(f)["data_columns"]
        __locations =__data_columns[3:]
        # __locations = [col.replace("location_", "") for col in __data_columns[3:]]
        
    global __model
    with open(r"D:\RKT\Python files\my projects\bang_lore_final_final\bhp_linear_model.pickle","rb") as f:
        __model=pickle.load(f)
    print("load artficats done ")

def get_location_names():
    return __locations

if __name__=="__main__":
    load_artifacts() 
    # print(get_location_names())
    
    print(get_price('1st block jayanagar',1000,3,3))
    # print(get_price('1st Phase JP Nagar',1000,2,3))
    print(get_price('1st block jayanagar',1000,3,2))
    print(get_price('1st block jayanagar',1500,2,2))
    print(get_price('1st block jayanagar',1500,2,1))