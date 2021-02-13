import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import timedelta
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import KFold

def set_arrival_date(func_df):
    #Add formatted timestamp column
    func_df['ReservationStatusDate'] = pd.to_datetime(func_df['ReservationStatusDate'], utc=False)

    func_df['ArrivalDate'] = pd.to_datetime(func_df.ArrivalDateMonth + ' ' + func_df.ArrivalDateDayOfMonth.astype(str) + ' ' + func_df.ArrivalDateYear.astype(str))

    func_df.ArrivalDateYear.astype(str)
    return func_df

def set_stay_length(func_df):
    #fill in length of stay if the status is check-out
    func_df.loc[(func_df['ReservationStatus'] == 'Check-Out'), 'ActualLengthOfStay'] = (func_df.ReservationStatusDate - func_df.ArrivalDate) / np.timedelta64(1, "D")

    #else, length of stay is 0
    func_df.loc[(func_df['ReservationStatus'] != 'Check-Out'), 'ActualLengthOfStay'] = 0

    #convert length of staty to integer
    func_df['ActualLengthOfStay'] = func_df['ActualLengthOfStay'].astype(int)

    #make feature for booked length of stay
    func_df['BookLengthOfStay'] = func_df.StaysInWeekendNights + func_df.StaysInWeekNights
    return func_df

def calculated_features(func_df):
    #calculate total cost of stay
    func_df['StayCost'] = func_df['ADR'] * func_df['BookLengthOfStay']

    #set binary if ADR is over hotel average for H1
    mask = (func_df.hotel == 'H1') & (func_df.ADR > 90)
    func_df.loc[mask, 'ADROverHotelAvg'] = 1
    mask = (func_df.hotel == 'H1') & (func_df.ADR <= 90)
    func_df.loc[mask, 'ADROverHotelAvg'] = 0

    #set binary if ADR is over hotel average for H2
    mask = (func_df.hotel == 'H2') & (func_df.ADR > 105)
    func_df.loc[mask, 'ADROverHotelAvg'] = 1
    mask = (func_df.hotel == 'H2') & (func_df.ADR <= 105)
    func_df.loc[mask, 'ADROverHotelAvg'] = 0
    return func_df

def filter_anomalies(func_df):
    #get rid of reservations booked for 0 nights
    mask = (func_df.StaysInWeekendNights == 0) & (func_df.StaysInWeekNights == 0)
    func_df = func_df[~mask]

    #mark reservations with 0 length of stay as IsCanceled = 1. They seemingly are erroneous "check-out"
    mask = (func_df.ReservationStatus == 'Check-Out') & (func_df.ActualLengthOfStay == 0)
    func_df.loc[mask, 'IsCanceled'] = 1
    func_df.loc[mask, 'ReservationStatus'] = 'Canceled'

    #seems odd to have more than 3 babies. set babies to max of 3
    func_df.loc[(func_df.Babies > 3), 'Babies'] = 3

    #same for children. set to max of 4
    func_df.loc[(func_df.Children > 4), 'Children'] = 4

    func_df['Children'] = func_df.Children.fillna(0)
    return func_df

def create_ohe_df(df, cat_list):
    '''
    One hot encoding for categorical variables
    '''
    cat_X = df.loc[:, cat_list]

    # ohe = OneHotEncoder(drop='first', sparse=False)
    ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)
    ohe_X = ohe.fit_transform(cat_X)
    columns = ohe.get_feature_names(cat_list)

    cat_df = pd.DataFrame(ohe_X, columns=columns, index=cat_X.index)

    df = pd.concat([df, cat_df], axis=1)

    df.drop(columns=cat_list, inplace=True)
    #print(df.shape)
    return df

def clean_data(func_df):
    func_df = set_arrival_date(func_df)

    func_df = set_stay_length(func_df)

    func_df = calculated_features(func_df)

    func_df = filter_anomalies(func_df)
    return func_df

def prep_data(func_df, cat_cols, drop_cols):
    func_df.drop(columns=drop_cols, inplace=True)

    func_df = create_ohe_df(func_df, cat_cols)
    return func_df

def match_df_cols(df1, df2):
    mask = df1.columns.isin(df2.columns)
    cols_index = list(df1.columns[~mask])
    if cols_index:
        print(f'Removed {cols_index} from df1')
        df1 = df1[df2.columns]

    mask = df2.columns.isin(df1.columns)
    cols_index = list(df2.columns[~mask])
    if cols_index:
        print(f'Removed {cols_index} from df2')

    return df1, df2

def transform_set(X_, Y_, cat_cols, drop_cols):
    full = X_.copy()
    full['IsCanceled'] = Y_

    full = clean_data(full)
    full = prep_data(full, cat_cols, drop_cols)

    X_ = full.drop(columns='IsCanceled')
    Y_ = full['IsCanceled']
    return X_, Y_

def run_cv(model, X_, Y_, n):
    kf = KFold(n_splits=n, shuffle=True, random_state = 71)
    cv_scores = [] #collect the validation results

    for train_ind, val_ind in kf.split(X_,Y_):
        X_train, y_train = X_[train_ind], Y_[train_ind]
        X_val, y_val = X_[val_ind], Y_[val_ind]

        model.fit(X_train, y_train)
        cv_scores.append(round(model.score(X_val, y_val), 3))

    print('Simple regression scores: ', cv_scores, '\n')
    return print(f'Simple mean cv score: {np.mean(cv_scores):.3f} +- {np.std(cv_scores):.3f}')

def last_minute_cancel(func_df):
    masks = [('actual_canceled',(func_df.IsCanceled == 1)),
            ('pred_true_pos',((func_df.predicted == 1) & (func_df.IsCanceled == 1)))]

    for mask_tup in masks:
        label, mask = mask_tup

        val_canceled = func_df[mask]
        val_canceled['LeadCancel'] = val_canceled.ArrivalDate - val_canceled.ReservationStatusDate
        print(label, 'total:', val_canceled.IsCanceled.count())
        cancel_df_blw15 = val_canceled[val_canceled.LeadCancel <= timedelta(days=14)]
        print(label, 'within 14 days:', cancel_df_blw15.shape[0])
    return
