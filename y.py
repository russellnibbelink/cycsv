import sqlite3
import csv
#conn = sqlite3.connect('cyclus100year.sqlite')
#c = conn.cursor()

def connDB(database_name):
    #error check
    global conn 
    conn = sqlite3.connect(database_name)
    global c 
    c = conn.cursor()
    return

def make_list(metric, table, order):
    #make_list(agentId, Agents, agentId)
    #basic sort DB
    mlist = []
    for row in c.execute('SELECT '+ metric + ' FROM ' + table + ' ORDER BY ' + order):
        mlist.append(row[0])
    return mlist

def make_sort_list(metric, table, order,filter_category, filter_metric):
    #make_sort_list('TransactionId', 'Transactions', 'Time', 'SenderId', 24)
    mlist = []
    for row in c.execute('SELECT '+ metric, Time +','+ filter_category + ' FROM ' + table + ' ORDER BY ' + order):
        if row[1] == filter_metric:
            mlist.append(row[0])
    return mlist

def test_list_1200():
    test = []
    i = 0
    while i < 1200:
        test.append(i)
        i += 1
    return test

#timing functions

#first function takes in metric, time

def time_sort1(metric, time, lst):
    lst[time // 12] += metric
    return

########

def time_sort2(tup):
    return

def test_list_1200_one():
    test = []
    i = 0
    while i < 1200:
        test.append(1)
        i += 1
    return test

def test_list_2400():
    test = []
    i = 0
    while i < 2400:
        test.append(i)
        i += 1
    return test

def avg_year(list_by_month):
    ylist = cumu_by_year(list_by_month)
    i = 0
    for elem in ylist:
        ylist[i] /= 12;
        i +=1;
    return ylist

def cumu_by_year(list_by_month):
    ylist = []
    i = 0
    total = 0
    for elem in list_by_month:
        total += elem
        i += 1
        if i % 12 == 0:
            ylist.append(total)
            total = 0
    return ylist

def cumulative(list_by_month):
    ylist = []
    i = 0
    total = 0
    for elem in list_by_month:
        total += elem
        i += 1
        if i % 12 == 0:
            ylist.append(total)
    return ylist

test1 = test_list_1200_one()
test2 = test_list_1200()
csv_test = cumulative(test1)

#get this to work -->
#to do: not all data is sampled exactly every month. Keep track of time stamp to determine the data points for each year. (determine when a year has passed).

def csv_w(data, name):
    #with open(name, 'w', newline='') as csvfile:
    with open(name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        for item in data:
            writer.writerow([item])
    return name

