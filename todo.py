todo_list=[]

def show_menu():
    print("\n---To-Do List Application---")
    print("1.Add task")
    print("2.View tasks")
    print("3.Delete task")
    print("4.Exit")
while True:
    show_menu()
    choice=input("\n Enter your choice (1-4): ")

    if choice=="4" :
        print("Thank you for using the app! Goodbye.")
        break

    elif choice=="1" :
        new_task=input("Input the enter task: ")
        todo_list.append(new_task)
        print(f"{new_task} Task added successfully!")

    elif choice=="2":
        if not todo_list:
            print("You to-do list is currently empty")
        else:
            print("--Your Current Tasks--")
            for index, task in enumerate(todo_list,1):           
                print(f"{index}. {task}")
                                                                                            # tasks automatically (1, 2, 3...) when displaying them on the screen.
    elif choice=="3":
        if not todo_list:
            print("There are no tasks to delete!")
        else:
            print("--Your Current Tasks--")
            for index, task in enumerate(todo_list,1):
                print(f"{index}. {task}")
            try:
                task_no=int(input("Enter the task number you want to delete: "))
                if 1<=task_no<=len(todo_list):
                    removed_task=todo_list.pop(task_no-1)
                    print(f"{removed_task} Task deleted successfully!")
                else:
                    print("Invalid task number!")     
            except ValueError:
                print("Invalid input! Please enter a valid task number.")        

    else:
        print("Invalid choice! Please enter a number between 1 and 4.")