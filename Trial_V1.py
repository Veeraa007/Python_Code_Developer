import arcpy
import pandas as pd

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\\GIS_Developer_Learnings\\Python\\Wales_UK.gdb"

Final_op = []

fc = arcpy.ListFeatureClasses()
for Features in fc:
    print(f" Features Classes : {Features}")

    Field = arcpy.ListFields(Features)

    for Fields in Field:
 #       print(Fields.name)
        Field_V1 = Fields.name
        if Field_V1 =="fclass" or Field_V1 =="type":

            unique_Value = {}
            with arcpy.da.SearchCursor(Features,[Field_V1]) as cur:

                for cursor in cur:
                    val = cursor[0]
                    unique_Value[val] = unique_Value.get(val,0)+1

            for value,count in unique_Value.items():

                    Final_op.append([arcpy.env.workspace,
                                    Features,
                                    Field_V1,
                                    value,
                                    count])

df = pd.DataFrame(Final_op,columns=["Gdbpath","Feature_class","Field","Unique_Value","Count"])
df.to_csv("D:\\books\\Trial_op.csv",index=False)


