import pandas as pd
import time
import csv

"""
Description
This program reads in file that is given from
the results of kmeans it has an iati identifier and a cluster number
The iati num is used to access raw data and corresponding
reporting org, sector, participating, geography data can be extracted.
this information is saved to the respective into cluster files.
"""

start = time.time()


global colhead, colhead2, data

data = pd.read_csv(
    "C:/corpus3/iati30Clusters.csv",
    dtype={"cluster30": int, "iati-identifier": str},
    encoding="utf-8",
)
# report = pd.read_csv("C:/corpus3/dfreport.csv", dtype={'df10rand.iati.identifier': str, 'df10rand.reporting.org': str, 'df10rand.reporting.org.ref':str, 'df10rand.reporting.org.type':str,	'df10rand.reporting.org.type.code':str},  encoding="ANSI")
colhead2 = list(data.columns)

report = pd.read_csv("C:/corpus3/dfcountry.csv", encoding="utf-8")
colhead = list(report.columns)
start = time.time()


def writetocsv(pfile, pline, phead):
    pfile = "C:/corpus3/" + pfile
    with open(pfile, mode="a", newline="", encoding="utf-8") as fw:
        file_writer = csv.writer(
            fw, lineterminator="\n", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        if phead:

            file_writer.writerow(pline)
        else:

            file_writer.writerow(pline)


def main():
    dict1 = {}
    for index, row in data.iterrows():
        if row[colhead2[0]] not in dict1:
            dict1[row[colhead2[0]]] = row[colhead2[1]]
    return dict1


def files():
    dictref = {}
    for i in range(31):
        dictref[i] = "cluster" + str(i) + ".csv"
        head = True
        writetocsv(dictref[i], colhead, head)

    return dictref


def getinfo(pdict1, pdict2, prep):
    head = False
    for index, row in prep.iterrows():
        if row[colhead[0]] in pdict1:
            clust = pdict1.get(row[colhead[0]])
            if int(clust) in pdict2:
                line = []
                for col in colhead:
                    line.append(row[col])
                writetocsv(pdict2.get(int(clust)), line, head)


retd1 = main()
retd2 = files()
getinfo(retd1, retd2, report)
