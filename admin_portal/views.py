from django.shortcuts import render
import pyodbc
import pandas as pd
import json

# conn_str = (
#     'Driver={SQL Server};'
#     'Server=localhots;'
#     'Database=elearn;'
#     'Trusted_Connection=yes;'
#     )
# cnxn = pyodbc.connect(conn_str)


# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=localhost;'
#                       'Database=elearn;'
#                       'UID=BI;'
#                       'Trusted_Connection=no;'
#                       )
try:
    conn_str = (
        r'Driver={ODBC Driver 17 for SQL Server};'  # Just an Example (SQL2008-2018)
        r'Server=localhost;' # Here you insert you servername
        r'Database=elearn;' # Here you insert your db Name
        r'Trusted_Connection=yes;' # This flag enables windows authentication
        )

    conn = pyodbc.connect(conn_str)
    if(conn):
        print("Connectd")
    else:
        print("Failed")

except Exception as ex:
    print(ex)
# Create your views here.
def index(request):
    return render(request,'index.html')


def logout_view(request):
    logout(request)
    return redirect('/admin_portal')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['emailid'] #username
        password = request.POST['Password'] #password
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print("loggedin")
            return redirect('/')
        else:
            print("error1")
    else:
        print("error2")
    return render(request,'admin_login.html')


def new_user(request):
    return render(request,'new_user.html')

def add_new_course(request):
    return render(request,'add_new_course.html')


def add_new_course_ajax(request):
    print("OK")
    if request.method == "POST":
        Course_Name = request.POST["Course_Name"]
        Start_Date = request.POST["Start_Date"]
        Class_Starting_Time = request.POST["Class_Starting_Time"]
        Class_Ending_Time = request.POST["Class_Ending_Time"]
        Doubt_Clearing_Session = request.POST["Doubt_Clearing_Session"]
        doubt_start_time = request.POST["doubt_start_time"]
        doubt_end_time = request.POST["doubt_end_time"]
        Actual_Price = request.POST["Actual_Price"]
        Offer_Price = request.POST["Offer_Price"]
        Overview = request.POST["Overview"]
        Description = request.POST["Description"]
        file_name = request.FILES["file"].name
        Catrgory = request.POST["Catrgory"]

        # For file Upload
        handle_uploaded_file_add_new_course(request.FILES["file"])
        sql = "insert into [dbo].[CourseDetails]([Course Name], [Start Date], [Class Starting Time], [Class Ending Time], [Doubt Clearing Session], [Doubt Starting Time], [Doubt Ending Time], [Actual Price], [Offer Price], [Course Overview], [Course Description], [Course Image], [Category], [Delete Status] ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = (Course_Name, Start_Date, Class_Starting_Time, Class_Ending_Time, Doubt_Clearing_Session, doubt_start_time ,doubt_end_time , Actual_Price, Offer_Price, Overview, Description , file_name , Catrgory , "No" )
        cursor = conn.cursor()
        cursor.execute(sql,params)
        print("Course Details Added Successfully")
        conn.commit()
    return render(request,"add_new_course.html")

    
def handle_uploaded_file_add_new_course(f):
    file_name = "elearnapp/static/images/course_images/"+str(f)
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def add_new_course_video(request):
    df_course = pd.read_sql("select [id],[Course Name] from [dbo].[CourseDetails]",conn)
    df_course.columns = df_course.columns.str.replace(' ', '')
    course_data = df_course.to_json(orient='records')
    course_data = json.loads(course_data)
    context = {"course_data":course_data}
    print(context)
    return render(request,'add_new_course_video.html',context)


def add_new_course_video_ajax(request):
    if request.method == "POST":
        Course_Id = request.POST["Course_Name"]
        Topic_Name = request.POST["Topic_Name"]
        video_link = request.POST["video_link"]
        sql = "insert into [dbo].[CourseVideos](course_id,Topic_Name,video_link,Delete_status) VALUES(?, ?, ?, ?)"
        params = (Course_Id , Topic_Name , video_link , "No" )
        cursor = conn.cursor()
        cursor.execute(sql,params)
        print("Video Details Added Successfully")
        conn.commit()



    return render(request,"add_new_course_video.html")