# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 11:37:37 2019

@author: USER
"""
import pandas as pd


def merge_inlinks(file, optional=None):
    data = pd.read_csv(file).fillna(1).replace(to_replace=0, value=1)
    optional_data = pd.read_csv(optional).fillna(1).replace(to_replace=0, value=1) if optional is not None else None

    if optional_data is not None:
        data = pd.concat([data, optional_data])

    groups = data.groupby(["Target URL", ])
    result = groups.agg('sum')
    result['Blended Score'] = result['SourceCitationFlow'] * result['SourceTrustFlow'] * result[
        'SourceTopicalTrustFlow_Value_0'] * (result['RefDomainTopicalTrustFlow_Value_0'] / 10)
    result.to_csv('Output/inlink_' + file.replace("Input/", ""), columns=['Blended Score'])


fresh = input('Path to fresh csv export: ')
hist = input('Path to historic csv export: ')
merge_inlinks(fresh, hist)