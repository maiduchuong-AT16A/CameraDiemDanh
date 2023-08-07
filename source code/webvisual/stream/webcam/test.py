str = "dataSet\\User.At160137.34.jpg"

Id = int((str.split("\\")[1].split('.')[1])[2:])
print(Id)