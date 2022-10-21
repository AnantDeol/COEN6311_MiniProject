import pandas as pd

#Variables for source files
employeedfpath = r"C:\Users\anant\OneDrive\Documents\MEngg\COEN 6311 Software\Mini Project\attachments (1)\EmployeeDatabase.csv"
taskdfpath = r"C:\Users\anant\OneDrive\Documents\MEngg\COEN 6311 Software\Mini Project\attachments (1)\TaskDatabase.csv"
notificationdfpath = r"C:\Users\anant\OneDrive\Documents\MEngg\COEN 6311 Software\Mini Project\attachments (1)\NotificationsDatabase.csv"

#Creating employee, task and notification database
employeedf=pd.read_csv(employeedfpath)
taskdf=pd.read_csv(taskdfpath)
notificationdf=pd.read_csv(notificationdfpath)  

#Saving the changes to csv
def savechanges():
    taskdf.to_csv(taskdfpath,index=False)
    employeedf.to_csv(employeedfpath,index=False)
    notificationdf.to_csv(notificationdfpath,index=False)
