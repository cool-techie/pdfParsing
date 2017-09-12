import tabula
import pandas as pd
import numpy as np

def rolling_group(val):
    if pd.notnull(val): rolling_group.group +=1 #pd.notnull is signal to switch group
    return rolling_group.group
rolling_group.group = 0 #static variable

def joinFunc(g,column):
    col =g[column]
    #joiner = "/" if column == "Action" else ","
    joiner = " "
    s = joiner.join([str(each) for each in col if pd.notnull(each)])
    #s = re.sub("(?<=&)"+joiner," ",s) #joiner = " "
    #s = re.sub("(?<=-)"+joiner,"",s) #joiner = ""
    #s = re.sub(joiner*2,joiner,s)    #fixes double joiner condition
    return s

def getDataframeHeaders(df):
    num_columns = len(df.columns)
    if num_columns == 2:
        return ["Index 0", "Index 1"]
    elif num_columns == 3:
        return ["Index 0", "Index 1", "Index 2"]

def getLastColumnHeader(df):
    num_columns = len(df.columns)
    return "Index " + str(num_columns-1)


df = tabula.read_pdf("/Users/mehrap/Desktop/ML_Stuff/US:CA Report/CA Sample Reports/HKGH0209242709.pdf", pages=1)
print(df)
df.columns = getDataframeHeaders(df)


#groups = df.groupby(df[getLastColumnHeader(df)].apply(rolling_group),as_index=False)
#groupFunct = lambda g: pd.Series([joinFunc(g,col) for col in g.columns],index=g.columns)
#print(groups.apply(groupFunct))

#for index, row in df.iterrows():
#    print(row[1], row[2], "\n")


