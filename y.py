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
    for row in c.execute('SELECT '+ metric + ", Time" +','+ filter_category + ' FROM ' + table + ' ORDER BY ' + order):
        if row[2] == filter_metric:
            mlist.append([row[0], row[1]])
    #print(mlist)
    return mlist

def make_raw_list(metric, table, order,filter_category, filter_list):
    #make_sort_list('TransactionId', 'Transactions', 'Time', 'SenderId', 24)
    mlist = []
    i = 0
    for row in c.execute('SELECT '+ metric +','+ filter_category + ' FROM ' + table + ' ORDER BY ' + order):
        if row[1] == filter_list[i][0]:
            mlist.append([row[0], filter_list[i][1]])
            #print(i)
            if i == len(filter_list)-1:
                break
            i+=1
    #print(mlist)
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

def time_sort(processed_data, year = 200):
    lst = [0] * year
    for tup in processed_data:
        index = tup[1] // 12
        lst[index] += tup[0]
    return lst

########


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

def csv_w(data, name):
    #with open(name, 'w', newline='') as csvfile:
    with open(name, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #writer.writerow(['Spam'] * 5 + ['Baked Beans'])
        for item in data:
            writer.writerow([item])
    return name


#get this to work -->
#to do: not all data is sampled exactly every month. Keep track of time stamp to determine the data points for each year. (determine when a year has passed).

### first metric
db_name = "cyclus200year.sqlite"
connDB(db_name)

sim_length = 200;

metric_name = "Uranium Mined"
metric_cat = "ResourceId"
data = "Quantity"
table_name = "Transactions"
data_table = "Resources"
category_name = "Commodity"
commodity_name = "nat_u"

raw_data = make_sort_list(metric_cat, table_name, 'Time', category_name, commodity_name)


## raw_data is a list of tuples [resourceId, time]
processed_data = make_raw_list(data, data_table, metric_cat, metric_cat, raw_data)

## correct data except its in months

out_data = time_sort(processed_data, sim_length)

csv_name = "Uranium_Mined.csv"
csv_w(out_data, csv_name)


### 



