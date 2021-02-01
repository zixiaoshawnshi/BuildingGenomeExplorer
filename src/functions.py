# this file contains a list of basic calculation functions

def calculate_hdd(df, base_temp, col):
    df['HDD'] = base_temp - df[col]
    df.loc[df['HDD'] < 0, 'HDD'] = 0
    return df['HDD']

def calculate_cdd(df, base_temp, col):
    df['CDD'] = df[col] - bsae_temp
    df.loc[df['CDD'] < 0, 'CDD'] = 0
    return df['CDD']
