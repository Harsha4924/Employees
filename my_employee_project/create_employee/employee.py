from django.db import connection
import base64

def get_email_address(email):
    sqlString = """select email from Employees where email=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[email])
            result = curs.fetchone()
            return result
    except Exception as e:
        print("An error occurred:", e)

def addEmployees(name,email,age,gender,phone,address_hno,address_street,address_city,address_state,base64_image):
    sqlString = """insert into Employees (name,email,age,gender,phone_no,hno,street,city,state,photo) values(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[name,email,age,gender,phone,address_hno,address_street,address_city,address_state,base64_image])
            connection.commit()
            curs.execute("SELECT LAST_INSERT_ID()")
            employee_id = curs.fetchone()[0]
            return employee_id
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        curs.close()

def addWork(add_user,company_name,from_date,to_date,address):
    sqlString = """insert into work_experience (user_id,companyname,from_date,to_date,work_address) values(
                %s, %s, %s, %s, %s)"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[add_user,company_name,from_date,to_date,address])
            connection.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")


def addProjects(add_user,title,theme):
    sqlString = """insert into projects (user_id,title,descriptions) values (
                %s, %s, %s)"""
    
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[add_user,title,theme])
            connection.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")


def addQualifications(add_user,qualification,grade):
    sqlString = """insert into all_qualifications (user_id,qualification,percentage) values (
                %s, %s, %s)"""
    print('boom',qualification)
    print('boom',grade)
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[add_user,qualification,grade])
            connection.commit()
    except Exception as e:
        print(f"Unexpected error: {e}")

def removeEmployee(emp_id):
    sqlString = """delete from Employees where id = %s"""

    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            connection.commit()
            return True
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    
def getEmployee(emp_id):
    sqlString = """select id from Employees where id = %s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            get_emp = curs.fetchone()
            return get_emp
    except Exception as e:
        print(f"Unexpected error: {e}")




def getEmployeedetails(emp_id):
    sqlString = """select name,email,age,gender,phone_no,hno,street,city,state,photo from Employees where id = %s"""
    l=[]
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            for record in curs:
                name = record[0]
                email = record[1]
                age = record[2]
                gender = record[3]
                mobile = record[4]
                house_no = record[5]
                street = record[6]
                city = record[7]
                state = record[8]
                # photo_data = record[9]

                # photo = base64.b64decode(photo_data).decode('utf-8') if photo_data else None

                l.append({'name':name,'email':email,'age':age,'gender':gender,'mobile':mobile,'house_no':house_no,'street':street,'city':city,'state':state})
            return l
    except Exception as e:
        print(f"Unexpected error boom: {e}")
        return False

def getEmployeeprojects(emp_id):
    l=[]
    sqlString = "select id, title, descriptions from projects where user_id = %s"
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            for record in curs:
                project_id = record[0]
                title = record[1]
                description = record[2]

                l.append({'project_id':project_id,'title':title,'description':description})
            return l
    except Exception as e:
        print(f"Unexpected error: {e}")

def getEmployeexperience(emp_id):
    l = []
    sqlString = """select id, companyname,from_date,to_date,work_address from work_experience where user_id = %s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            for record in curs:
                work_id = record[0]
                company = record[1]
                from_date = record[2]
                to_date = record[3]
                work_address = record[4]
                l.append({'work_id':work_id,'company':company,'from_date':from_date,'to_date':to_date,'work_address':work_address})
            return l
    except Exception as e:
        print(f"Unexpected error: {e}")

def getEmployeequalifications(emp_id):
    l=[]
    sqlString = """select id, qualification, percentage from all_qualifications where user_id = %s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString,[emp_id])
            for record in curs:
                id = record[0]
                qualification = record[1]
                percentage = record[2]
                l.append({'id':id,'qualification':qualification,'percentage':percentage})
            return l
    except Exception as e:
        print(f"Unexpected error: {e}")

def updateEmployee(name, email, age, gender, phone, address_hno, address_street, address_city, address_state, emp_id):
    sqlString = """update Employees set name=%s, email=%s, age=%s, gender=%s, phone_no=%s, hno=%s, street=%s, city=%s, state=%s WHERE id=%s"""
    try:
        with connection.cursor() as curs:
            curs.execute(sqlString, [name, email, age, gender, phone, address_hno, address_street, address_city, address_state, emp_id])
            connection.commit()
            return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    

def getAllemployees():
    sqlString = """select id, name, email from Employees"""
    employee_list = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sqlString)
            for record in cursor:
                id = record[0]
                name = record[1]
                email = record[2]
                employee_list.append({'id': id, 'name': name, 'email': email})
            # employee_list.append({'id': id, 'name': name, 'email': email})
            return employee_list
    except Exception as e:
        print("An error occurred while fetching employees:", e)
        return None
