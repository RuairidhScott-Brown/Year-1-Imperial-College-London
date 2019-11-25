#!/usr/bin/env python3
import csv

# read flash.dat to a list of lists
datContent = [i.strip().split(' ') for i in open("/home/ruairidh/Documents/ICL/1st_year/materials/stress_strain_hardening/group_11/composite.dat").readlines()]

# write it as a new CSV file
with open("composite.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(datContent)
