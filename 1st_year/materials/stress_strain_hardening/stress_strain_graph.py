#! /usr/bin/env python3

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import math
import collections
from statistics import mean

def strain_data():
    excel_file = '/home/ruairidh/Documents/ICL/1st_year/materials/stress_strain_hardening/strain_measurements.xlsx'
    raw_data = pd.read_excel(excel_file, sheetname = 1)
    return raw_data
    #print(raw_data.head())

def strain_calculations(raw_data):
    V_in =  1.265
    gauge_factor = 2.1
    gain = 500
    constant = 4/(V_in*gauge_factor*gain)
    area = {'copper': [((0.00597/2)**2)*math.pi], 'brass':[((0.00593/2)**2)*math.pi], 'aluminium':[((0.00597/2)**2)*math.pi]}
    voltages = raw_data.drop("force", axis="columns")
    columns = list(voltages)
    strain = collections.OrderedDict()
    strain["al_loading_strain"] = []
    strain["al_unloading_strain"] = []
    strain["brass_loading_strain"] = []
    strain["brass_unloading_strain"] = []
    strain["cu_loading_strain"] = []
    strain["cu_unloading_strain"] = []
    columns_strain = list(strain.keys())
    stress = {"al_stress": [], "brass_stress": [], "cu_stress": []}
    for k in raw_data.index:
        stress["al_stress"] += [((raw_data["force"][k]*1000)/area['aluminium'][0])/10000000]
        stress["brass_stress"]+= [((raw_data["force"][k]*1000)/area['brass'][0])/10000000]
        stress["cu_stress"]+= [((raw_data["force"][k]*1000)/area['copper'][0])/10000000]
    stress = pd.DataFrame(stress)

    for i, j in zip(columns, columns_strain):
            for m in raw_data.index:
                strain[j] += [constant*raw_data[i][m]]
    strain = pd.DataFrame(strain)
    frames = [raw_data, stress,strain]
    stress_vs_strain = pd.concat(frames, axis=1)
    return stress_vs_strain

def graph_2(stress_vs_strain,  m_al, b_al, m_brass, b_brass, m_cu, b_cu):
    regression_line_al = [(m_al*x)+b_al for x in stress_vs_strain["al_loading_strain"]]
    regression_line_brass = [(m_brass*j)+b_brass for j in stress_vs_strain["brass_loading_strain"]]
    regression_line_cu = [(m_cu*k)+b_cu for k in stress_vs_strain["cu_loading_strain"]]

    fig, ax = plt.subplots(1,3, sharey =True)
    ax[0].scatter(stress_vs_strain["al_loading_strain"], stress_vs_strain["al_stress"])
    ax[0].plot(stress_vs_strain["al_loading_strain"], regression_line_al)
    ax[0].set(xlim=(-0.0001,0.0017))
    ax[0].set_title("Aluminium")
    ax[0].set_ylabel("Stess (MPa)")


    ax[1].scatter(stress_vs_strain["brass_loading_strain"], stress_vs_strain["brass_stress"])
    ax[1].plot(stress_vs_strain["brass_loading_strain"], regression_line_brass)
    ax[1].set(xlim=(-0.0001,0.0017))
    ax[1].set_title("Brass")
    ax[1].set_xlabel("Strain")

    ax[2].scatter(stress_vs_strain["cu_loading_strain"], stress_vs_strain["cu_stress"])
    ax[2].plot(stress_vs_strain["cu_loading_strain"], regression_line_cu)
    ax[2].set(xlim=(-0.0001,0.0017))
    ax[2].set_title("Copper")

    plt.suptitle("Stress vs Strain", fontsize = 15)
    fig.autofmt_xdate()
    plt.show()

    
def line_of_best_fit(data):
    m_al = (((mean(data["al_loading_strain"])*mean(data["al_stress"])) - mean(data["al_loading_strain"]*data["al_stress"]))/((mean(data["al_loading_strain"])**2)- mean(data["al_loading_strain"]**2)))
    b_al = mean(data["al_stress"]) - m_al*mean(data["al_loading_strain"])
    m_brass = (((mean(data["brass_loading_strain"])*mean(data["brass_stress"])) - mean(data["brass_loading_strain"]*data["brass_stress"]))/((mean(data["brass_loading_strain"])**2)- mean(data["brass_loading_strain"]**2)))
    b_brass = mean(data["brass_stress"]) - m_brass*mean(data["brass_loading_strain"])
    m_cu = (((mean(data["cu_loading_strain"])*mean(data["cu_stress"])) - mean(data["cu_loading_strain"]*data["cu_stress"]))/((mean(data["cu_loading_strain"])**2)- mean(data["cu_loading_strain"]**2)))
    b_cu = mean(data["cu_stress"]) - m_cu*mean(data["cu_loading_strain"])
    return m_al, b_al, m_brass, b_brass, m_cu, b_cu


def graph_1(raw_data):
    fig, stress_gauge = plt.subplots(1,3, sharey = True)
    al_loading, = stress_gauge[0].plot(raw_data["al_loading"], raw_data["force"])
    al_unloading, = stress_gauge[0].plot(raw_data["al_unloading"], raw_data["force"])
    stress_gauge[0].set_title("Aluminium")
    stress_gauge[0].set_ylabel("Force (kN)")
    stress_gauge[0].set(xlim=(0,0.6))

    brass_loading = stress_gauge[1].plot(raw_data["brass_loading"], raw_data["force"])
    brass_unloading = stress_gauge[1].plot(raw_data["brass_unloading"], raw_data["force"])
    stress_gauge[1].set_title("Brass")
    stress_gauge[1].set_xlabel("Amplified Voltage (V)")
    stress_gauge[1].set(xlim=(0,0.6))


    cu_loading = stress_gauge[2].plot(raw_data["cu_loading"], raw_data["force"])
    cu_unloading = stress_gauge[2].plot(raw_data["cu_unloading"], raw_data["force"])
    stress_gauge[2].set_title("Copper")
    stress_gauge[2].set(xlim=(0,0.6))

    fig.legend((al_loading, al_unloading), ('Loading', 'Unloading'), frameon = False, loc = 'lower center', ncol = 2)
    plt.suptitle("Force vs Amplified Voltage", fontsize = 15)
    plt.show()


def tenstion_data():
    aluminium_excel = '/home/ruairidh/Documents/ICL/1st_year/materials/stress_strain_hardening/group_11/al_stress_strain_failure.xlsx'
    raw_aluminium = pd.read_excel(aluminium_excel, sheetname = 0)
    composite_excel = '/home/ruairidh/Documents/ICL/1st_year/materials/stress_strain_hardening/group_11/composite.xlsx'
    raw_composite = pd.read_excel(composite_excel, sheetname = 0)
    polymer_excel = '/home/ruairidh/Documents/ICL/1st_year/materials/stress_strain_hardening/group_11/poly_stress_strain_failure.xlsx'
    raw_polymer = pd.read_excel(polymer_excel, sheetname = 0)
    raw_aluminium = raw_aluminium.dropna()
    raw_aluminium.columns = ['time', 'mm', 'kN','strain', 'N/mm^2', 'digits', 'nominal strain', 'nominal stress', 'true strain', 'true stress']
    raw_composite = raw_composite.dropna()
    raw_composite.columns = ['time', 'mm', 'kN','strain', 'N/mm^2', 'digits', 'nominal strain', 'nominal stress', 'true strain', 'true stress']
    raw_polymer = raw_polymer.dropna()
    raw_polymer.columns = ['time', 'mm', 'kN','strain', 'N/mm^2', 'digits', 'nominal strain', 'nominal stress', 'true strain', 'true stress']
    return raw_aluminium, raw_composite, raw_polymer

def trendline(raw):
    return False
def graph_3_nominal(aluminium, composite, polymer):
    fig, ax = plt.subplots(1,3)
    ax[0].scatter(aluminium['nominal strain'], aluminium['nominal stress']/10000000)
    ax[0].set(ylim = (-0.5,25))
    ax[0].set_ylabel("Stress (MPa)")
    ax[0].set_title("Aluminium")

    ax[1].scatter(composite['nominal strain'], composite['nominal stress']/10000000)
    ax[1].set(xlim=(-0.005, 0.03), ylim=(-5,80))
    ax[1].set_title("Composite")
    ax[1].set_xlabel("Strain")


    ax[2].scatter(polymer['nominal strain'], polymer['nominal stress']/10000000)
    ax[2].set(xlim=(-0.05, 0.45), ylim=(-0.5, 6.5))
    ax[2].set_title("Polymer")

    plt.suptitle("Nominal Stess vs Strain", fontsize =15 )
    fig.autofmt_xdate()
    plt.show()

def graph_3_true(aluminium, composite, polymer):
    regression_line_poly = [((555437314.998022/10000000)*x)+(2356348.99896217/10000000) for x in polymer["true strain"]]
    regression_line_composite = [((36580513163.4834/10000000)*i)+(-49377671.2510246/10000000) for i in composite["true strain"]]
    regression_line_al = [((17582773310.107/10000000)*k)+(-63441404.008927/10000000) for k in aluminium["true strain"]]







    fig, ax = plt.subplots(1,3)
    ax[0].scatter(aluminium['true strain'], aluminium['true stress']/10000000)
    ax[0].scatter(aluminium['nominal strain'], aluminium['nominal stress']/10000000, color = 'r')
    ax[0].plot(aluminium["true strain"], regression_line_al)
    ax[0].axhline(y=21.8, color = 'r')
    ax[0].axvline(x=0.049958, color = 'r')
    ax[0].set(ylim = (-0.5,30))
    ax[0].set_ylabel("Stress (MPa)")
    ax[0].set_title("Aluminium")

    ax[1].scatter(composite['true strain'], composite['true stress']/10000000)
    ax[1].scatter(composite['nominal strain'], composite['nominal stress']/10000000, color = 'r')
    ax[1].plot(composite["true strain"], regression_line_composite)
    ax[1].set(xlim=(-0.005, 0.03), ylim=(-5,80))
    ax[1].set_title("Composite")
    ax[1].set_xlabel("Strain")


    ax[2].scatter(polymer['true strain'], polymer['true stress']/10000000)
    ax[2].scatter(polymer['nominal strain'], polymer['nominal stress']/10000000, color = 'r')
    ax[2].plot(polymer["true strain"], regression_line_poly)
    ax[2].set(xlim=(-0.05, 0.45), ylim=(-0.5, 9))
    ax[2].set_title("Polymer")

    plt.suptitle("True Stess vs Strain", fontsize =15 )
    fig.autofmt_xdate()
    plt.show()




if '__main__' == __name__:
    raw_data = strain_data()
    graph_1(raw_data)
    calculated_data = strain_calculations(raw_data)
    m_al, b_al, m_brass, b_brass, m_cu, b_cu = line_of_best_fit(calculated_data)
    graph_2(calculated_data, m_al, b_al, m_brass, b_brass, m_cu, b_cu)
    print(calculated_data)
    print(m_al, b_al, m_brass, b_brass, m_cu, b_cu)
    aluminium, composite, polymer =  tenstion_data()
    graph_3_nominal(aluminium, composite, polymer)
    graph_3_true(aluminium, composite, polymer)


    



    