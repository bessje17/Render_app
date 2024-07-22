# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 10:16:28 2024

@author: Jeanne
"""

def determine_season(i_month):
    """
    Match a month as an integer with its season as a string
    :param i_month: Month as an integer
    :type i_month: integer
    :return: Season as a string
    :rtype: str

    """
    if i_month in [10,11,12,1,2,3]:
        return "Automne-Hiver"
    else:
        return "Printemps-Eté"