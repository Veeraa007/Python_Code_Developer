
import arcpy
import pandas as pd

arcpy.env.workspace = r"D:\\GIS_Developer_Learnings\\Python\\Wales_UK.gdb"
arcpy.env.overwriteOutput = True

data =[]
def list_field(target_field):
    
    fc = arcpy.ListFeatureClasses()
    for Feature in fc:
        field = arcpy.ListFields(Feature)
        for field1 in field:
            print(field1.name)
            f1 =field1.name
            if f1 in target_field:
                dbf(Feature,f1)
def dbf(Feature,f1):
    uni_val ={}
    with arcpy.da.SearchCursor(Feature,[f1]) as cur:
        for val in cur:
            value =val[0]
            uni_val[value] = uni_val.get(value,0)+1
    
    for value, count in uni_val.items():
                
                #print(f"{str(value):<20} {str(count):<20}")
                data.append([
                arcpy.env.workspace,
                Feature,
                f1,
                value, 
                count
                ])
list_field(['fclass','type'])

df = pd.DataFrame(data,columns=["Gdbpath","Feature_class","Field","Unique_Value","Count"])
df.to_csv("D:\\books\\Trial_1_op.csv",index=False)
#print("done")



