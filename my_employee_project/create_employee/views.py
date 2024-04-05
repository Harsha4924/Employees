from django.shortcuts import render
from django.http import HttpResponse
from . import employee
from django.http import JsonResponse
import base64

# Create your views here.

#this is the home page, the add employee, remove employee, get employee, get all employees buttons will be visible
def home(request):
    return render(request,'create_employee/home.html')

#the employee will add all the details in this page
def add_employee(request):
    return render(request,'create_employee/addemployee.html')

#after submitting the employee details this function will add all the details in to the database(MYSQL)
def submit_form(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            address_hno = request.POST.get('address[hno]')
            address_street = request.POST.get('address[street]')
            address_city = request.POST.get('address[city]')
            address_state = request.POST.get('address[state]')
            image = request.FILES.get('photo')
            image_data = image.read()
            base64_image = base64.b64encode(image_data)

            get_email = employee.get_email_address(email)
            #this will check if the email is present in the database. 
            if get_email:
                return JsonResponse({"message": "Employee already exists", "success": False})

            add_user = employee.addEmployees(name,email,age,gender,phone,address_hno,address_street,address_city,address_state,base64_image)

            work_experiences = []
            current_work = {}
            for key,value in request.POST.items():
                if 'work_experience' in key:
                    start_index = key.find('[')+1
                    end_index = key.find(']')
                    work_index = int(key[start_index:end_index])
                    if 'company' in key:
                        current_work[work_index] = {'company':value}
                    elif 'from_date' in key:
                        current_work[work_index]['from_date'] = value
                    elif 'to_date' in key:
                        current_work[work_index]['to_date'] = value
                    elif 'address' in key:
                        current_work[work_index]['address'] = value

            for index, j in current_work.items():
                company_name = j.get('company')
                from_date = j.get('from_date')
                to_date = j.get('to_date')
                address = j.get('address')
                employee.addWork(add_user,company_name,from_date,to_date,address)
                work_experiences.append(j)

            projects = []
            current_project = {}
            for key, value in request.POST.items():
                if 'projects' in key:
                    index_start = key.find('[') + 1
                    index_end = key.find(']')
                    project_index = int(key[index_start:index_end])
                    if 'title' in key:
                        current_project[project_index] = {'title': value}
                    elif 'description' in key:
                        current_project[project_index]['description'] = value

            for index, project_data in current_project.items():
                title = project_data.get('title')
                theme = project_data.get('description')
                employee.addProjects(add_user,title,theme)
                projects.append(project_data)

            qualify = []
            current_qualification = {}
            for key,value in request.POST.items():
                if 'qualifications' in key:
                    first_index = key.find('[')+1
                    last_index = key.find(']')
                    qualify_index = int(key[first_index:last_index])
                    if 'qualify_name' in key:
                        current_qualification[qualify_index] = {'qualification_name' : value}
                    elif 'percentage' in key:
                        current_qualification[qualify_index]['percentage'] = value

            for i, j in current_qualification.items():
                qualification = j.get('qualification_name')
                grade = j.get('percentage')
                employee.addQualifications(add_user,qualification,grade)
                qualify.append(j)

            return JsonResponse({"message": "Employee Created Successfully", "success": True})

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return JsonResponse({"message": "An error occurred : Employee creation failed", "success": False})



# the user needs to enter the employee id to remove the employee
def remove_employee(request):
    return render(request,'create_employee/removeemployee.html')


#this function will fetch all the details of the employee based on the entered employee id
def get_employee(request):
    if request.method == "POST":
        try:
            emp_id = request.POST.get('user_id')

            check_user = employee.getEmployee(emp_id)
            if check_user is None:
                return JsonResponse({"message":"Employee with this ID does not exist", "success": False})
            else:
                try:
                    employee_details = employee.getEmployeedetails(emp_id)
                except Exception as e:
                    return JsonResponse({"message": f"Error fetching employee details: {str(e)}", "success": False})
                
                try:
                    employee_projects = employee.getEmployeeprojects(emp_id)
                except Exception as e:
                    return JsonResponse({"message": f"Error fetching employee projects: {str(e)}", "success": False})
                
                try:
                    employee_work = employee.getEmployeexperience(emp_id)
                except Exception as e:
                    return JsonResponse({"message": f"Error fetching employee work experience: {str(e)}", "success": False})
                
                try:
                    employee_qualifications = employee.getEmployeequalifications(emp_id)
                except Exception as e:
                    return JsonResponse({"message": f"Error fetching employee qualifications: {str(e)}", "success": False})

                return render(request, 'create_employee/getemployee.html', {'context': True, 'employee_details': employee_details, 'employee_projects': employee_projects, 'employee_work': employee_work, 'employee_qualifications': employee_qualifications})
        except Exception as e:
            return JsonResponse({"message": f"An error occurred: {str(e)}", "success": False})

    return render(request, 'create_employee/getemployee.html')


# this function will remove the particular employee based on the employee id
def remove_employeefrom_db(request):
    if request.method == 'POST':
        try:
            emp_id = request.POST.get('emp_id')

            check_user = employee.getEmployee(emp_id)
            if check_user is None:
                return JsonResponse({"message":"Employee with this ID doesnot exist", "success": False})
            else:
                delete_emp = employee.removeEmployee(emp_id)
                if delete_emp:
                    return JsonResponse({"message":"Employee Deleted SuccessFully", "success": True})
        except Exception as e:
            return JsonResponse({"message": "An error occurred while removing the employee", "success": False})
        

#this function will updates the employee details based on the employee id
def update_employee(request):
    if request.method == 'POST':
        try:
            emp_id = request.POST.get('employee_id')

            check_user = employee.getEmployee(emp_id)
            if check_user is None:
                return JsonResponse({"message":"Employee with this ID does not exist", "success": False})
            else:
                try:
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    age = request.POST.get('age')
                    gender = request.POST.get('gender')
                    phone = request.POST.get('phone')
                    address_hno = request.POST.get('address_hno')
                    address_street = request.POST.get('address_street')
                    address_city = request.POST.get('address_city')
                    address_state = request.POST.get('address_state')
                    update = employee.updateEmployee(name,email,age,gender,phone,address_hno,address_street,address_city,address_state,emp_id)
                    if update:
                        return JsonResponse({"message": "Employee details updated successfully", "success": True})
                    else:
                        return JsonResponse({"message": "Employee Updation Failed", "success": False})
                except Exception as e:
                    return JsonResponse({"message": "An error occurred while updating the employee", "success": False})
        except Exception as e:
            return JsonResponse({"message": "An error occurred", "success": False})
        
    return render(request, 'create_employee/updatemployee.html')

#this function will fetches all the employees from the database.
def get_all_employees(request):
    try:
        check = employee.getAllemployees()
        if check is not None:
            return render(request, 'create_employee/getallemployees.html', {'check': check})
    except Exception as e:
        return JsonResponse({"message": "An error occurred while retriving the employees details", "success": False})