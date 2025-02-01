import arcpy
import pandas as pd


class GISFeatureAnalyzer:
    def __init__(self, workspace, output_csv):
        self.workspace = workspace
        self.output_csv = output_csv
        arcpy.env.workspace = self.workspace
        arcpy.env.overwriteOutput = True
        self.data = []

    def analyze_feature_classes(self, target_fields):
        # Get all feature classes in the workspace
        feature_classes = arcpy.ListFeatureClasses()
        if not feature_classes:
            print("No feature classes found in the workspace.")
            return

        # Iterate through each feature class
        for feature_class in feature_classes:
            print(f"Processing feature class: {feature_class}")
            fields = arcpy.ListFields(feature_class)

            for field in fields:
                if field.name in target_fields:
                    self._process_field(feature_class, field.name)

    def _process_field(self, feature_class, field_name):

        value_count = {}

        try:
            with arcpy.da.SearchCursor(feature_class, [field_name]) as cursor:
                for row in cursor:
                    val = row[0]
                    value_count[val] = value_count.get(val,0)+1

            for value, count in value_count.items():
                print(f"{str(value):<20} {str(count):<20}")
                self.data.append([
                    self.workspace,
                    feature_class,
                    field_name,
                    value,
                    count
                ])
        except Exception as e:
            print(f"Error processing field '{field_name}' in '{feature_class}': {e}")

    def save_to_csv(self):
     
        if not self.data:
            print("No data to save.")
            return

        try:
            df = pd.DataFrame(self.data, columns=["DB_Name", "FeatureClass", "Field", "Unique_value", "Count"])
            df.to_csv(self.output_csv, index=False)
            print(f"Data successfully saved to {self.output_csv}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")


if __name__ == "__main__":
    workspace = r"D:\\GIS_Developer_Learnings\\Python\\Wales_UK.gdb"
    output_csv = r"D:\\GIS_Developer_Learnings\\Python\\op9.csv"
    target_fields = ["fclass", "type"]

    analyzer = GISFeatureAnalyzer(workspace, output_csv)
    analyzer.analyze_feature_classes(target_fields)
    analyzer.save_to_csv()
