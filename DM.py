from datetime import datetime

import GM
import DataSources

employeedf=DataSources.employeedf
taskdf=DataSources.taskdf
notificationdf=DataSources.notificationdf
savechanges=DataSources.savechanges

#General variables
errormessage="\n Wrong input, please try again.\n"
now=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


class department_manager(GM.general_manager):
    def __init__(self, id, paswd, validips):
        super().__init__(id, paswd, validips)

    def viewtasks(self):
        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        print(taskdf.loc[taskdf.Department==empdept,['Task_name','TaskID','Status','Assigned_to','Task_assign_date']].reset_index(drop=True))

    def assigntask(self, taskid, empid):
        
        if taskid == None:
            taskid=input('Enter Task ID: ')
        else:
            pass

        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        taskdf1=taskdf.loc[taskdf.Department==empdept]
        
       
        if taskid in taskdf1['TaskID'].values.tolist():

            #Fetching task details
            task_to_be_assigned_id = taskdf[taskdf['TaskID']==taskid].index.values[0]
            task_to_be_assigned_id_status = taskdf.loc[task_to_be_assigned_id,'Status']

            empid=input('Enter the Employee ID whom you want to assign this task to: ')

            if empid in employeedf['EmployeeID'].values.tolist():

                #Fetching task details
                email_input_index=employeedf[employeedf['EmployeeID']==empid].index.values[0]   
                email_input_role= employeedf.loc[email_input_index,'Role']
                email_input_dept = employeedf.loc[email_input_index,'Department']
            
                if (email_input_role == "Worker" or email_input_role == "Department Manager") and email_input_dept == empdept:
                
                    #Assign new task
                    if  task_to_be_assigned_id_status == "unassigned":
                        countoftasks = len(taskdf[taskdf["Assigned_to"] == empid].index.values)

                        if countoftasks >= 3:
                            print("\nYou cannot assign more than 3 tasks to this worker\n")
                        else:
                            GM.general_manager.assigntask(self,taskid,empid)
                
                    #Reassign Task
                    else:
                        countoftasks = len(taskdf[taskdf["Assigned_to"] == empid].index.values)

                        if countoftasks >= 3:
                            print("\nYou cannot assign more than 3 tasks to this worker\n")
                        else:
                            notificationdf.loc[len(notificationdf.index)]={'NotificationType':'Reassign','AssignedBy':self.id,'TaskID':taskid,'AssignedTo':empid,'Department':empdept,'Status':"Pending",'Date':datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                            savechanges()
                            print("\nRequest to reasign task sent to the General Manager\n")

                elif email_input_role == "Worker" and email_input_dept != empdept:
                    print("\nSorry! you cannot assign tasks to employees who belong to a different department\n")

                elif email_input_role == "Department Manager":
                    print("\nSorry! you cannot assign tasks to your peer managers\n")

                elif email_input_role == "General Manager":
                    print("\nSorry! you cannot assign tasks to the general manager\n")

                else:
                    print("\nInvalid input!\n")

            else:
                print("\nInvalid employee id\n")

        else:
            print("\nInvalid Task ID\n")

    def canceltask(self):
        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        taskdf1=taskdf.loc[taskdf.Department==empdept]
        
        taskid=input('Enter Task ID: ')
        if taskid in taskdf1['TaskID'].values.tolist():                   
            task_to_be_cancelled_index = taskdf[taskdf['TaskID']==taskid].index.values[0]
            empid = taskdf.loc[task_to_be_cancelled_index,'Assigned_to']
            empindex= employeedf[employeedf['EmployeeID']==empid].index.values[0]
            empdept= employeedf.loc[empindex,'Department']

            notificationdf.loc[len(notificationdf.index)]={'NotificationType':"Cancelled",'Actioned_by':self.id,'Actioned_by_role':'Department Manager','TaskID':taskid,'EmployeeID':empid,'Department':empdept,'Date':datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),'Status':'Pending'}
            savechanges()
            print("\nRequest to cancel task sent to the General Manager\n")

        else:
            print('\nInvalid TaskID\n')

    def view_notifications(self):
        empindex= employeedf[employeedf['EmployeeID']==self.id].index.values[0]
        empdept= employeedf.loc[empindex,'Department']
        notificationdf1=notificationdf.loc[(notificationdf['Status'] != "Pending") & (notificationdf['ReadByDM'] != "Yes") & (notificationdf['Department'] == empdept),['NotificationType','Date','Status','TaskID','AssignedTo','AssignedBy','Department']].reset_index(drop=True)
        
        print(notificationdf1)
        notificationdf.loc[(notificationdf['Status'] != "Pending") & (notificationdf['ReadByDM'] != "Yes") & (notificationdf['Department'] == empdept), 'ReadByDM'] = "Yes"
        savechanges()

    def change_task_status(self):
        usertasks=taskdf[taskdf['Assigned_to']==self.id]
        print(usertasks)
        taskid=input('Enter the task ID')

        if taskid not in usertasks.TaskID.tolist():
            print("Invalid Task ID\n")
        else:
            while True:
                try:
                    task_changed_status_ip=int(input('Select new status:\n1.Pending\n2.Resolved\n'))

                except ValueError:
                    print(errormessage)
                    continue

                if task_changed_status_ip not in [1,2]:
                    print(errormessage)
                    continue

                else:
                    taskindex= taskdf[taskdf['TaskID']==taskid].index.values[0]
                    if task_changed_status_ip==1:
                        task_changed_status='Pending'
                    else:
                        task_changed_status='Resolved'
                    
                    taskdf.loc[taskindex,'Status']=task_changed_status
                    
                    #Saving the changes to csv
                    savechanges()
                    print("\nDone!\n")
                    break




