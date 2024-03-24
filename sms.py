import pyodbc as odbccon
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
conn = odbccon.connect(
    "Driver={SQL Server};"
    "Server=loki;"
    "Database=student_management_system;"
    "Trusted_Connection=yes;")
cursor = conn.cursor()

def columns():
    cursor.execute('select * from student')
    a = [description[0] for description in cursor.description]
    b = {}
    for i in range(len(a)):
        b[i] = a[i]
    x=len(max(list(b.values()),key=len))
    c=""
    for i in range(len(b)):
        if i%2==0:
            c=c+f"{i}. "+b[i]+" "*(x-len(b[i])+5)
        if i%2!=0:
            c=c+f"{i}. "+b[i]+"\n"
    return b,c

def get_details():
    register_no=int(input("enter reg_no: "))
    fullname=(input("enter your fullname: ")).upper()
    gender=input("enter your gender: ").upper()
    dob=input("enter your dob: ")
    email=input("enter your email: ").lower()
    dep_name=input("enter your depatmnent(shortform): ").upper()
    current_year=input("enter current year: ")
    section=input("enter your section: ").upper()
    course_complete_year=input("enter course_completition_year: ")
    mobile=input("enter your mobile no: ")
    address=input("enter your adress: ").upper()

    cursor.execute('insert into student(register_no,fullname,gender,dob,email,dep_name,current_year,section,course_complete_year,mobile,address) values(?,?,?,?,?,?,?,?,?,?,?);',(
        register_no,fullname,gender,dob,email,dep_name,current_year,section,course_complete_year,mobile,address))
    conn.commit()
    print("\n")
def display():
    # cursor.execute('SELECT * from student')
    # for row in cursor:
    #     print(row)
    # conn.commit()
    # print("\n")
    df = pd.read_sql('select * from student', conn)
    print(df.to_string())
    print("\n")

def filter_students():
    b,c=columns()
    print(c)
    select = int(input("enter the columns(0-10):"))
    if select==0:
        select=int(select)
    filter_by=b[select]
    name=input(f"filter by {b[select]}: ")
    if name.isdigit()!=True:
        name="'"+name+"'"

    sql=f'select * from student where {filter_by}={name}'
    r=cursor.execute(sql).fetchall()
    df = pd.read_sql(sql, conn)
    print(df.to_string(),r)
    print("\n")
    # for row in cursor:
    #     print(list(row))
    # conn.commit()

def sort_students():
    b,c=columns()
    print(c)
    select = int(input("short by column(0-10):"))
    order_cols=b[select]
    aord={1:'asc',2:'desc'}
    select1 = int(input(f"1.ascending\t2.descending\nshort by column(0-10):"))
    order_by=aord[select1]
    sql=f'select * from student order by {order_cols} {order_by}'
    r=cursor.execute(sql).fetchall()
    df=pd.read_sql(sql,conn)
    print(df.to_string(),r)
    print("\n")
    # for row in cursor:
    #     print(row)
    # conn.commit()

def delete_students():
    reg_no = int(input("enter the register_no you want to delete: "))
    cursor.execute("delete from student where register_no=?",reg_no)
    conn.commit()
    print("successfully deleted")
    print("\n")

def update_students():
    b,c=columns()
    update_register = int(input("enter rg_no of whose data you want to update: "))
    print(c)
    select = input("enter the columns you want to update seperated by comma(,):")
    select=select.split(',')
    c = []
    for i in select:
        if i.isdigit():
            c.append(int(i))

    for i in c:
        dat = input(f"update {b[i]}: ")
        if b[i]!='email':
            dat=dat.upper()
        if dat!=update_register:
            dat = "'" + dat + "'"
        cursor.execute(f'update student set {b[i]}={dat} where register_no={update_register}')
    conn.commit()
    print("successfully updated.")
    print("\n")

while True:
    print("___________\n|   MENU  |\n-----------\n1.insert details\t2.display\t3.filter\n4.delete\t\t\t5.sortby\t6.update\n7.exit")
    choose=int(input("\nchoose any one option: "))
    if choose==1:
        get_details()
    elif choose==2:
        display()
    elif choose==3:
        filter_students()
    elif choose==4:
        delete_students()
    elif choose==5:
        sort_students()
    elif choose==6:
        update_students()
    elif choose==7:
        break