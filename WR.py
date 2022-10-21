from datetime import datetime

import DM
import DataSources

employeedf=DataSources.employeedf
taskdf=DataSources.taskdf
notificationdf=DataSources.notificationdf
savechanges=DataSources.savechanges

#General variables
errormessage="\n Wrong input, please try again.\n"
now=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

class worker(DM.department_manager):
    def __init__(self, id, paswd, validips):
        super().__init__(id, paswd, validips)

    def viewtasks(self):
        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        print(taskdf.loc[(taskdf.Department==empdept) & (taskdf.Status=='unassigned'),['Task_name','TaskID','Status','Assigned_to','Task_assign_date']].reset_index(drop=True))

    
    def assigntask(self):
        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        taskdf1=taskdf.loc[taskdf.Department==empdept]

        if len(taskdf[taskdf["Assigned_to"] == self.id].index.values)>=3:
            print('\n You already have 3 tasks assigned\n')

        else:
            taskid=input('Enter Task ID: ')

            if taskid in taskdf1['TaskID'].values.tolist():

                taskindex = taskdf[taskdf['TaskID']==taskid].index.values[0]
                task_to_be_assigned_status = taskdf.loc[taskindex,'Status']
            
                if task_to_be_assigned_status == "unassigned":
                    empid = self.id
                    taskindex= taskdf[taskdf['TaskID']==taskid].index.values[0]
                    employeeindex=employeedf[employeedf['EmployeeID']==self.id].index.values[0]
                    tasks_assigned=int(employeedf.loc[employeeindex,'#tasks_assigned'])
            
                    #Applying changes to dataframe
                    taskdf.loc[taskindex,'Assigned_to']=empid
                    taskdf.loc[taskindex,'Task_assign_date']=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                    taskdf.loc[taskindex,'Status']="assigned"
                    taskdf.loc[taskindex,'Assigned_by']=self.id

                    employeedf.loc[employeeindex,'#tasks_assigned']=tasks_assigned+1

                    notificationdf.loc[len(notificationdf.index)]={'Action':'assign','Actioned_by':self.id,'Actioned_by_role':'Worker','TaskID':taskid,'EmployeeID':empid,'Department':empdept,'Date':datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}

                    #Saving the changes to csv
                    savechanges()
                    print("\nDone!\n")

                elif task_to_be_assigned_status == "assigned":
                    print("\n Sorry, this task is already assigned\n")

                else:
                    print("Invalid Task ID\n")

            else:
                print("Invalid Task ID\n")

    def change_task_status(self):
        return super().change_task_status()