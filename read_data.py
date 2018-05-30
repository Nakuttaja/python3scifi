# -*- coding: utf-8 -*-

# Reads data from measurement and retuns the data in a dataframe.
# The device measured the frequency of particles in a specific channel,
# which corresponds to a specific energy. Data was in an excel spreadsheet.


import openpyxl
import pandas as pd


def read(sheet):
    """ Read the data from excel worksheet and return a dataframe.
        This function uses openpyxl library, which is handy for reading excel
        worksheets. It also uses pandas library, which contains a dataframe
        function where we can store the data.
        
        return: dataframe of the data
    """    
    
    FILE_PATH = 'data/mittaukset.xlsx'
    file = openpyxl.load_workbook(FILE_PATH)
    
    sheet = file.worksheets[sheet]
    data = sheet['A2000': 'B2500']  # Relevant data is in this range
    
    # These values are from calibrating the device. Values link the channel
    # and the corresponding energy in form of y = kx + b
    slope = 0.02237
    constant = -0.00886163

    energies = []
    fqs = []
    
    for channel, frequency in data:
        energy = slope*channel.value + constant # Calculate the energy
        energies.append(energy)
        fqs.append(frequency.value)
        
    # Dataframe looks like this (x = energy, y = frequency):
    # index    x      y
    #   .      .      .
    #   .      .      .   
    #   .      .      .
    #   .      .      .

    df = pd.DataFrame()
    df['x']=energies
    df['y']=fqs
    
    return df
