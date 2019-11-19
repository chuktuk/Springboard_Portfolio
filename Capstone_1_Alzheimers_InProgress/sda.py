#!/usr/bin/env python3
"""Statistical data analysis module for Alzheimer's Capstone 1.

This module contains functions used to extract data for and to perform
statistical analysis on the ADNI Alzheimer's Disease dataset for my
Capstone project. Inputs for these functions can be obtained using 
adnidatawrangling module, and some additional wrangling from the eda module.
Required modules for all functions to run: pandas, numpy, matplotlib.pyplot,
seaborn all using standard namespaces.
"""

if 'pd' not in globals():
    import pandas as pd

if 'np' not in globals():
    import numpy as np
    
if 'plt' not in globals():
    import matplotlib.pyplot as plt
    
if 'sns' not in globals():
    import seaborn as sns
    
sns.set()

def get_deltadx_groups():
    """This function uses the final_exam dataframe to divide the data by diagnosis change.
    
    The groups returned by this function are no_change, cn_mci, mci_ad, and cn_ad.
    """
    
    # isolate patients with no diagnosis change
    no_change = final_exam[final_exam['DX'] == final_exam['DX_bl2']]
    
    # isolate patients who progressed from 'CN' to 'AD'
    cn_mci = final_exam[(final_exam['DX'] == 'MCI') & (final_exam['DX_bl2'] == 'CN')]
    
    # isolate patients who progressed from 'MCI' to 'AD'
    mci_ad = final_exam[(final_exam['DX'] == 'AD') & (final_exam['DX_bl2'] == 'MCI')]
    
    # isolate patients who progressed from 'CN' to 'AD'
    cn_ad = final_exam[(final_exam['DX'] == 'AD') & (final_exam['DX_bl2'] == 'CN')]
    
    return no_change, cn_mci, mci_ad, cn_ad

def divide_genders(df):
    """This function divides the supplied dataframe by the 'PTGENDER' column.
    
    Returns two dataframes: males, females.
    """
    
    males = df[df.PTGENDER == 'Male']
    females = df[df.PTGENDER == 'Female']
    
    return males, females

def test_gender_effect(df, biomarker, size):
    """This function returns the p value for the test that males/females have the 
    
    same distribution for the change in the supplied biomarker. The test will be 
    performed over 'size' permutations. A significant p value means that males/females 
    should be separated for further analysis of change in in the supplied biomarker. 
    A high p value means males/females can be considered together.
    """
    
    # create a combined array for the biomarker
    c_arr = np.array(df[biomarker])
    
    # divide the data by gender
    fe_males = df[df.PTGENDER == 'Male']
    fe_females = df[df.PTGENDER == 'Female']

    # get counts of the number of males and females
    num_males = df.PTGENDER.value_counts()['Male']
    num_females = df.PTGENDER.value_counts()['Female']
    
    # calculate the observed mean difference
    obs_mean_diff = np.mean(fe_males[biomarker]) - np.mean(fe_females[biomarker])
    
    # initialize empty numpy array
    perm_mean_diffs = np.empty(size)
    
    # run the permutations calculating means each time
    for i in range(size):
        r_arr = np.random.permutation(c_arr)
        null_arr1 = r_arr[:num_males]
        null_arr2 = r_arr[num_males:]
        perm_mean_diffs[i] = np.mean(null_arr1) - np.mean(null_arr2)
    
    # calculate and display p value
    p = np.sum(perm_mean_diffs >= obs_mean_diff) / len(perm_mean_diffs)
    print('Distribution Test for Males/Females')
    print('Variable: ', biomarker)
    print('If p < 0.05, then split the data by gender')
    print('p-value: ', p)