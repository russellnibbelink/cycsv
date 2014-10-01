import sqlite3
#ask about the :memory: to create a Database in RAM
conn = sqlite3.connect('cyclus.sqlite')


c = conn.cursor()

# Create table
#c.execute('''CREATE TABLE stocks
#             (date text, trans text, symbol text, qty real, price real)''')

# Insert a row of data
#c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
#print (c.fetchone())

# Larger example that inserts many records at a time
purchases = [('2006-03-28', 'BUY', 'GOOG', 700, 89.00),
             ('2006-04-05', 'BUY', 'APPL', 800, 79.00),
             ('2006-04-06', 'SELL', 'YHOO', 200, 34.00),
            ]
#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

i = 0
p_to_l = 0
list0 = [0,0]
list1 = [0,0]
list2 = [0,0]
list3 = [0,0]
inception = [list0, list1, list2, list3]

for row in c.execute('SELECT qty, price FROM stocks ORDER BY price'):
    i = i + 1
    inception[p_to_l][0] = inception[p_to_l][0] + row[0]
    inception[p_to_l][1] = inception[p_to_l][1] + row[1]
    if i % 12 == 0:
        print(len(inception[p_to_l]))
        p_to_l = p_to_l + 1

print(inception)
        

    
#print()
#r = ('Region',)
#c.execute('SELECT * FROM AgentEntry WHERE  Kind = ?', r)
#p = c.fetchone()
#print(p)
#print(p[1])

#c.execute('''
    #CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT,
                       #phone TEXT, email TEXT unique, password TEXT)
#''')
#INTEGER PRIMARY KET and TEXT unique have to be unique
#c.execute("INSERT INTO users VALUES (11, 'Bob', 'Android', 'bobby', 'password')")
#c.execute('DROP TABLE users')


# Save (commit) the changes
conn.commit()