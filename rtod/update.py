import sys

if len(sys.argv) != 4:
    print("usage : python3 update.py <old file> <new file> <output file>")
    quit()

fold = sys.argv[1]
fnew = sys.argv[2]
fout = sys.argv[3]

f1 = open(fold, "r")
f2 = open(fnew, "r")

var1 = []
path1 = []
db1 = {}
wid1 = []

var2 = []
path2 = []
db2 = {}
wid2 = []

def inter(lst1, lst2):
    lst3 = [value for value in lst2 if value[0:8] in lst1]
    return lst3

def diff(lst1, lst2):
    lst3 = [value for value in lst2 if value.split(',')[0].split('/')[1] not in lst1]
    return lst3

#var1 contains all variables in order :
#ARGO_OBSERVATION_ID,PLATFORM_NUMBER,ARGO_POSITION_LATITUDE,ARGO_POSITION_LONGITUDE,DATE_OF_DATASENT,POSITION_INDICATOR_OF_ARGO,CYCLE_NUMBER,RECORD_COUNT,DATA_MODE

for i in f1:
    word1 = i
    if word1[0] == '#' :
        continue 
    
    var1 = word1.split(',')
    if var1[0] == 'ARGO_OBSERVATION_ID':
        continue

    mode = var1[-1][0]

    dateid = var1[0].split('_')
    
    wmoid = dateid[0]
    wid1.append(wmoid)
    
    date = dateid[1]
    date = date.replace("-", "")
    
    added = 0
    if mode == 'R':
        for key in db1.keys():
            if key == wmoid:
                db1[wmoid].append(date)
                added = 1
                break
        if added == 0:
            db1[wmoid] = [date]

#we dont require to check repetations in old file
wid1 = list(set(wid1))  

f1.close()

#var2 contains all variables in order :
#file,date,latitude,longitude,ocean,profiler_type,institution,date_update
#i divided file into  4 parts, 3 : filename, 012 : path

rows = []
index = 0

for i in f2:
    word2 = i
    if word2[0] == '#' :
        continue 
    
    var2 = word2.split(',')
    if var2[0] == 'file':
        rows.append(i)
        index+=1
        continue

    path2 = var2[0].split('/')
    wmoid = path2[1]
    fname = path2[3]
    date = var2[1][0:8]

    ocean = 'I' 
#indian ocean 

    added = 0
    if var2[4] == ocean:
        wid2.append(i)
        if fname[0] == 'D': 
            rows.append(i)
            for key in db2.keys():
                if key == wmoid:
                    db2[wmoid].append(date+'_'+str(index))
                    added = 1
                    break
            if added == 0:
                db2[wmoid] = [date+'_'+str(index)]
            index+=1

f2.close()

db3 = {}

for key in db1.keys():
    try :
        db3[key] = inter(db1[key], db2[key])
    except Exception as e:
        continue

#takes care of new instances
#wmoids that exist in file 2, but not in file 1
wid = []
wid = diff(wid1, wid2)

#noRepRows takes care of repetations
noRepRows = []

for key in db3.keys():
    for values in db3[key]:
        noRepRows.append(rows[int(values[9:])][:-1])

noRepRows = list(set(noRepRows))

#writing in files here
f3 = open(fout, "w")

f3.write(rows[0])

for line in noRepRows:
    f3.write("%s\n" %line)

for line in wid:
    f3.write(line)

f3.close()
