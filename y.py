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
    mlist = []
    i = 0
    if (len(filter_list) == 0): 
        return [[0, 0]]
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

###General Variables
db_name = "cyclus200year.sqlite"
connDB(db_name)
sim_length = 200;

### uranium mined

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


######------------ Electricity Generated ----------#######

#### functions for electricity generated #####
def IO_raw(metric, table, order,filter_category, filter_metric):
    mlist = []
    for row in c.execute('SELECT '+ metric + ", EnterTime, ExitTime" +','+ filter_category + ' FROM ' + table + ' ORDER BY ' + order):
        if row[3] == filter_metric:
            mlist.append([row[0], row[1], row[2]])
    #print(mlist)
    return mlist

def IO_list(metric, table, order,filter_category, filter_list):
    mlist = []
    i = 0
    if (len(filter_list) == 0): 
        return [[0, 0, 0]]
    for row in c.execute('SELECT '+ metric +','+ filter_category + ' FROM ' + table + ' ORDER BY ' + order):
        if row[1] == filter_list[i][0]:
            mlist.append([row[0], filter_list[i][1], filter_list[i][2]])
            if i == len(filter_list)-1:
                break
            i+=1
    return mlist

def IO_time_sort(processed_data, year = 200):
    lst = [0.0] * year
    i = 0
    for year in lst:
        for arr in processed_data:
            if arr[1] <= i*12 and arr[2] > i*12:
                year += arr[0]
        lst[i] = year*12/1000
        i+=1
    return lst

lookup_list_LWR = IO_raw("AgentId", "Facilities", "AgentId", "Prototype", "LWR")
lookup_list_SFR = IO_raw("AgentId", "Facilities", "AgentId", "Prototype", "SFR")
lookup_list_MOX = IO_raw("AgentId", "Facilities", "AgentId", "Prototype", "MOX")

lookup_list_LWR = IO_list("out_commod_cap", "AgentState_cycamore_BatchReactorInfo", "AgentId", "AgentId", lookup_list_LWR)
lookup_list_SFR = IO_list("out_commod_cap", "AgentState_cycamore_BatchReactorInfo", "AgentId", "AgentId", lookup_list_SFR)
lookup_list_MOX = IO_list("out_commod_cap", "AgentState_cycamore_BatchReactorInfo", "AgentId", "AgentId", lookup_list_MOX)

LWR_out = IO_time_sort(lookup_list_LWR)
SFR_out = IO_time_sort(lookup_list_SFR)
MOX_out = IO_time_sort(lookup_list_MOX)

LWR_csv_name = "LWR_Electicity_Generated.csv"
csv_w(LWR_out, LWR_csv_name)

SFR_csv_name = "SFR_Electricity_Generated.csv"
csv_w(SFR_out, SFR_csv_name)

MOX_csv_name = "MOX_Electricity_Generated.csv"
csv_w(MOX_out, MOX_csv_name)

########---- UNFULLFILLED DEMAND

demand = [200]*200

LWR_csv_name = "LWR_Unfulfilled_Demand.csv"
csv_w([i - j for i, j in zip(demand, LWR_out)], LWR_csv_name)

SFR_csv_name = "SFR_Unfulfilled_Demand.csv"
csv_w([i - j for i, j in zip(demand, SFR_out)], SFR_csv_name)

MOX_csv_name = "MOX_Unfulfilled_Demand.csv"
csv_w([i - j for i, j in zip(demand, MOX_out)], MOX_csv_name)

#######------ CAPACITY STARTED -----
#if its what I think not hard at all

#######------ CAPACITY ENDED ------
#ditto

########-------FUEL LOADED -------- ########

LWR_fuel_loaded = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "fresh_lwr_fuel")
LWR_fuel_loaded = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", LWR_fuel_loaded)
LWR_FL_out = time_sort(LWR_fuel_loaded)
LWR_FL_name = "LWR_Fuel_Loaded.csv"
csv_w(LWR_FL_out, LWR_FL_name)

SFR_fuel_loaded = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "fresh_sfr_fuel")
SFR_fuel_loaded = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", SFR_fuel_loaded)
SFR_FL_out = time_sort(SFR_fuel_loaded)
SFR_FL_name = "SFR_Fuel_Loaded.csv"
csv_w(SFR_FL_out, SFR_FL_name)

MOX_fuel_loaded = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "fresh_mox_fuel")
MOX_fuel_loaded = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", MOX_fuel_loaded)
MOX_FL_out = time_sort(MOX_fuel_loaded)
MOX_FL_name = "MOX_Fuel_Loaded.csv"
csv_w(MOX_FL_out, MOX_FL_name)

#########---------FUEL LOADED ------- #######
LWR_UNF_rep = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "rep_lwr_tru")
LWR_UNF_rep = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", LWR_UNF_rep)
LWR_rep_out = time_sort(LWR_UNF_rep)
LWR_rep_name = "LWR_Reprocessed.csv"
csv_w(LWR_rep_out, LWR_rep_name)

SFR_UNF_rep = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "rep_sfr_tru")
SFR_UNF_rep = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", SFR_UNF_rep)
SFR_rep_out = time_sort(SFR_UNF_rep)
SFR_rep_name = "SFR_Reprocessed.csv"
csv_w(SFR_rep_out, SFR_rep_name)

MOX_UNF_rep = make_sort_list("ResourceId", "Transactions", "Time", "Commodity", "rep_mox_tru")
MOX_UNF_rep = make_raw_list("Quantity", "Resources", "ResourceId", "ResourceId", mox_UNF_rep)
MOX_rep_out = time_sort(MOX_UNF_rep)
MOX_rep_name = "MOX_Reprocessed.csv"
csv_w(MOX_rep_out, MOX_rep_name)



