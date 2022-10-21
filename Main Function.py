import GM
import DM
import DataSources
import WR

from datetime import datetime

#Creating Dataframes 
employeedf=DataSources.employeedf
taskdf=DataSources.taskdf
notificationdf=DataSources.notificationdf

#General variables
errormessage="\n Wrong input, please try again.\n"
now=datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


if __name__ == '__main__':


    while True:

        print("Welcome to Task Management Portal")
        loginid=input('Please enter your email ID\n')
        loginpwd=input('Please enter your password\n')

        #Check if id and password are valid
        if loginid in employeedf['EmployeeID'].values.tolist():
            empindex=employeedf[employeedf['EmployeeID']==loginid].index.values[0]
            emprole= employeedf.loc[empindex,'Role']

            if loginpwd==employeedf.loc[empindex,'Password']:
                pass
                
            else:
                print('Incorrect password\n')
                continue
        else:
            print("Invalid email ID\n")
            continue
            
        #Actions as per role
        if emprole=="General Manager":
            LoginUser= GM.general_manager(loginid,loginpwd,[1,2,3,4,5,6])

            while True:
                try:
                    actionvar=int(input("Select your action:\n1. View all tasks\n2. View Employee database\n3. Assign Task\n4. Cancel Task\n5. View notifications\n6. Log out\n"))
                except ValueError:
                    print(errormessage)
                    continue

                if actionvar not in LoginUser.validips:
                    print(errormessage)
                    continue
                        
                #View all tasks
                elif actionvar==1: 
                    LoginUser.viewtasks()
                    continue

                #View employee database
                elif actionvar==2:
                    LoginUser.viewemployees()
                    continue

                #Assign Task
                elif actionvar==3:
                    LoginUser.assigntask(None,None)
                                                        
                #Cancel Task
                elif actionvar==4:
                    LoginUser.canceltask(None)

                #View Notifications
                elif actionvar==5:
                    LoginUser.view_notifications()

                #Log out
                elif int(actionvar)==6:
                    loginid=None
                    loginpwd=None
                    break
        
        elif emprole=="Department Manager":
            LoginUser= DM.department_manager(loginid,loginpwd,[1,2,3,4,5,6,7])

            while True:
                try:
                    actionvar=int(input("Select your action:\n1. View all tasks\n2. View Employee database\n3. Assign Task\n4. Cancel Task\n5. View notifications\n6. Change task status\n7. Log out\n"))
                except ValueError:
                    print(errormessage)
                    continue

                if actionvar not in LoginUser.validips:
                    print(errormessage)
                    continue

                elif actionvar==1: 
                    LoginUser.viewtasks()
                    continue

                #View employee database
                elif actionvar==2:
                    LoginUser.viewemployees()
                    continue

                #Assign Task
                elif actionvar==3:
                    LoginUser.assigntask(None,None)                                        

                #Cancel Task
                elif actionvar==4:
                    LoginUser.canceltask()

                #View notifications
                elif actionvar==5:
                    LoginUser.view_notifications()

                #Change task status
                elif int(actionvar)==6:
                    LoginUser.change_task_status()

                #Log out
                elif int(actionvar)==7:
                    loginid=None
                    loginpwd=None
                    break

        elif emprole=="Worker":
            LoginUser= WR.worker(loginid,loginpwd,[1,2,3,4])

            while True:
                try:
                    actionvar=int(input("Select your action:\n1. View all tasks\n2. Assign Task\n3. Change task status\n4. Log out\n"))
                except ValueError:
                    print(errormessage)
                    continue

                if actionvar not in LoginUser.validips:
                    print(errormessage)
                    continue

                else:
                        
                    #View all tasks
                    if actionvar==1: 
                        LoginUser.viewtasks()
                        continue

                    #Assign Task
                    elif actionvar==2:
                        LoginUser.assigntask()

                    #Change task status
                    elif int(actionvar)==3:
                        LoginUser.change_task_status()

                    #Log out
                    elif int(actionvar)==4:
                        loginid=None
                        loginpwd=None
                        break       

        #Return to Login option               
        continue
            