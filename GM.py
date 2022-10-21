import numpy as np
from datetime import datetime
import datetime as dt
import DataSources

#Reading employee, task and notification database
employeedf=DataSources.employeedf
taskdf=DataSources.taskdf
notificationdf=DataSources.notificationdf
savechanges=DataSources.savechanges

#General variables
errormessage="\n Wrong input, please try again.\n"
now=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

#Creating GM's class
class general_manager:

    def __init__(self,id,paswd,validips):
        self.id=id
        self.paswd=paswd
        self.validips=validips
     
    def viewtasks(self):
        return print(taskdf[['Task_name','TaskID','Status','Assigned_to','Task_assign_date']].reset_index(drop=True))

    def viewemployees(self):
        return print(employeedf[['Employee_Name','EmployeeID','Role','Department','#tasks_assigned']])

    def assigntask(self,taskid,empid):
        
        if taskid == None:
            taskid=input('Enter Task ID: ')
        else:
            pass
            
        if taskid in taskdf['TaskID'].values.tolist():
            if empid==None:
                empid=input('Enter the Employee ID whom you want to assign this task to: ')
            else:
                pass
            if empid in employeedf['EmployeeID'].values.tolist():
                taskindex= taskdf[taskdf['TaskID']==taskid].index.values[0]
                empdept = taskdf.loc[taskindex,'Department']
                employeeindex=employeedf[employeedf['EmployeeID']==empid].index.values[0]
                tasks_assigned=int(employeedf.loc[employeeindex,'#tasks_assigned'])
            
                #Applying changes to dataframe
                taskdf.loc[taskindex,'Assigned_to']=empid
                taskdf.loc[taskindex,'Task_assign_date']=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                taskdf.loc[taskindex,'Status']="assigned"
                taskdf.loc[taskindex,'Assigned_by']=self.id

                employeedf.loc[employeeindex,'#tasks_assigned']=tasks_assigned+1

                notificationdf.loc[len(notificationdf.index)]={'NotificationType':'Assigned','AssignedBy':self.id,'TaskID':taskid,'AssignedTo':empid,'Department':empdept,'Date':now}

                #Saving the changes to csv
                savechanges()
                print("\nDone!\n")
            
            else:
                print("Invalid employee id\n")
                
        else:
            print("Invalid Task ID\n")
    
    def canceltask(self,taskid):
        if taskid == None:
            taskid=input('Enter Task ID: ')
        else:
            pass
        if taskid in taskdf['TaskID'].values.tolist():              
            taskindex= taskdf[taskdf['TaskID']==taskid].index.values[0]
            empdept = taskdf.loc[taskindex,'Department']
            if taskdf.loc[taskindex,'Status']=="unassigned":
                return print("\n Cannot cancel task that has not been assigned yet\n")
            else:
                empid=taskdf.loc[taskindex,'Assigned_to']
                employeeindex= employeedf[employeedf['EmployeeID']==empid].index.values[0]
                tasks_assigned=int(employeedf.loc[employeeindex,'#tasks_assigned'])

            taskdf.loc[taskindex,'Task_assign_date']=np.nan
            taskdf.loc[taskindex,'Assigned_to']=np.nan
            taskdf.loc[taskindex,'Assigned_by']=np.nan
            taskdf.loc[taskindex,'Status']="unassigned"

            employeedf.loc[employeeindex,'#tasks_assigned']=tasks_assigned-1
            notificationdf.loc[len(notificationdf.index)]={'NotificationType':'Cancelled','AssignedBy':self.id,'TaskID':taskid,'AssignedTo':empid,'Department':empdept,'Date':datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
            #Saving the changes to csv
            savechanges()
            print("\nDone!\n")
        else:
                print("Invalid Task ID\n")

    def view_notifications(self):
        
        print("Following are the tasks that have been assigned or cancelled: \n\n",
            notificationdf.loc[(notificationdf['Status'] != "Pending") & (notificationdf['ReadByGM'] != "Yes"),['NotificationType','Date','Status','TaskID','AssignedTo','AssignedBy','Department']].reset_index(drop=True),"\n\n",
            "Following are the tasks that require your approval: \n\n",
            notificationdf.loc[(notificationdf['Status'] == "Pending"),['NotificationType','Date','Status','TaskID','AssignedTo','AssignedBy','Department']].reset_index(drop=True))
    
        notificationdf.loc[(notificationdf['Status'] != "Pending") & (notificationdf['ReadByGM'] != "Yes"), 'ReadByGM'] = "Yes"
    
        takeaction= int(input('Do you wish to approve a request?\n1.Yes\n2.No\n'))
        if takeaction==1:
            actionables = notificationdf[(notificationdf['Status'] == "Pending")].reset_index(drop=True)
            print(actionables['TaskID'].values.tolist())
            
            while True:
                    taskid= input('\nPlease enter the taskid from the list above\n')
                
                    if taskid in actionables['TaskID'].values.tolist():
                        req_index = actionables[actionables['TaskID']==taskid].index.values[0]
                        if actionables.loc[req_index,'NotificationType']=='Reassign':
                            
                            notempid=actionables.loc[req_index,'AssignedTo']
                            notindex=notificationdf[(notificationdf['TaskID']==taskid) & (notificationdf['Status']=='Pending')].index.values[0]
                            taskindex=taskdf[taskdf['TaskID']==taskid].index.values[0]
                            empid=taskdf.loc[taskindex,'Assigned_to']
                            employeeindex= employeedf[employeedf['EmployeeID']==empid].index.values[0]
                            tasks_assigned=int(employeedf.loc[employeeindex,'#tasks_assigned'])

                            notificationdf.loc[notindex,'Status']='Approved'
                            employeedf.loc[employeeindex,'#tasks_assigned']=tasks_assigned-1
                            
                            savechanges()
                            self.assigntask(taskid,notempid)
                            
                            break

                        elif actionables.loc[req_index,'NotificationType']=='Cancelled':
                            taskid=actionables.loc[req_index,'TaskID']
                            notindex=notificationdf[(notificationdf['TaskID']==taskid) & (notificationdf['Status']=='Pending')].index.values[0]
                            notificationdf.loc[notindex,'Status']='Approved'
                            self.canceltask(taskid)
                           
                            savechanges()
                            break

                        else:
                            print(errormessage)
                            continue
                    
                    else:
                        print('\n Invalid Task ID\n')
                        break
            
        elif takeaction==2:
            savechanges()
        else:
            print("Wrong Input")

    
        
    
    
