#! /usr/bin/env/ python3
import csv

# read flash.dat to a list of lists
datContent = [i.strip().split() for i in open("./flash.dat").readlines()]

# write it as a new CSV file
with open("/group_11/composite.dat", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(datContent)
