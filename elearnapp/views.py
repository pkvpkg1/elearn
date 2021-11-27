from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import statistics 
import json
import pandas as pd
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.mail import send_mail
import os
import glob
import schedule
import time
import xlrd
from django.contrib.auth import get_user_model
from datetime import datetime
import numpy as np
from django.core.files.storage import FileSystemStorage
import pyodbc
from datetime import datetime
import razorpay
from django.http import HttpResponseBadRequest
 


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


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
    return redirect('/')

def login_user(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['emailid'] #username
        password = request.POST['Password'] #password
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print("loggedin")
            return redirect('/')
            # if request.GET["next"]:
            #     id_get=request.GET["id"]
            #     url = str(request.GET["next"]) + "?id=" + str(id_get)
            #     return redirect(url)
            # else:
            #     return redirect('/')
        else:
            context = {"error":"error"}
            print("error1")
    else:
        print("error2")
    return render(request,'login.html',context)


def new_user(request):
    return render(request,'new_user.html')


def new_user_ajax(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["emailid"]
        Password = request.POST["Password"]      
        user = User.objects.create_user(email, email, Password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        print("Success")
        
    return render(request,'new_user.html')


def my_courses(request):
    df_orders = pd.read_sql("select *  from [dbo].[orders] as a left join [dbo].[CourseDetails] as b on a.course_id = b.id where email='"+str(request.user.username)+"';",conn)
    df_orders.columns = df_orders.columns.str.replace(' ', '')
    course_data = df_orders.to_json(orient='records')
    course_data = json.loads(course_data)
    print(df_orders)
    context = {"course_data":course_data}
    

    return render(request,'my_courses.html',context)


def course_video_watch(request):
    if request.method == "GET":
        id_get = request.GET["id"]
        df_course = pd.read_sql("select [Course Name] from [dbo].[CourseDetails] where [Delete Status]='No' and Id='"+id_get+"'",conn)
        df_course.columns = df_course.columns.str.replace(' ', '')
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)

        vid_id = request.GET["vid_id"]
        video_select = pd.read_sql("select * from [dbo].[CourseVideos] where [Delete_status]='No' and course_id='"+id_get+"' and id='"+vid_id+"'",conn)
        video_select.columns = video_select.columns.str.replace(' ', '')
        Video_course_data = video_select.to_json(orient='records')
        Video_course_data = json.loads(Video_course_data)

        df_course_videos = pd.read_sql("select * from [dbo].[CourseVideos] where [Delete_status]='No' and course_id='"+id_get+"'",conn)
        df_course_videos.columns = df_course_videos.columns.str.replace(' ', '')
        df_course_videos_data = df_course_videos.to_json(orient='records')
        df_course_videos_data = json.loads(df_course_videos_data)

        context = {"course_title":course_data[0]["CourseName"], "df_course_videos_data":df_course_videos_data, "id_get":id_get,"video_link":Video_course_data[0]["video_link"] }

    return render(request,'course_video_watch.html',context)



def course_video_watch_first(request):
    if request.method == "GET":
        id_get = request.GET["id"]
        df_course = pd.read_sql("select [Course Name] from [dbo].[CourseDetails] where [Delete Status]='No' and Id='"+id_get+"'",conn)
        df_course.columns = df_course.columns.str.replace(' ', '')
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)

        df_course_videos = pd.read_sql("select * from [dbo].[CourseVideos] where [Delete_status]='No' and course_id='"+id_get+"'",conn)
        df_course_videos.columns = df_course_videos.columns.str.replace(' ', '')
        df_course_videos_data = df_course_videos.to_json(orient='records')
        df_course_videos_data = json.loads(df_course_videos_data)

        context = {"course_title":course_data[0]["CourseName"], "df_course_videos_data":df_course_videos_data, "id_get":id_get}

    return render(request,'course_video_watch_first.html',context)







def forget_password(request):
    return render(request,'forget_password.html')



def contact(request):
    return render(request,'contact.html')

    
def courses(request):
    df_course = pd.read_sql("select * from [dbo].[CourseDetails] where [Delete Status]='No'",conn)
    df_course = df_course.rename({'Course Name': 'CourseName', 'Actual Price': 'ActualPrice','Offer Price':'OfferPrice',"Course Overview":"CourseOverview","Course Image":"CourseImage"}, axis=1)
    course_data = df_course.to_json(orient='records')
    course_data = json.loads(course_data)
    print(type(course_data))
    context = {"course_data":course_data}

    return render(request,'courses.html',context)


    
def courses_view(request):
    context = {}
    if request.method == "GET":
        id_get = request.GET["id"]
        df_course = pd.read_sql("select * from [dbo].[CourseDetails] where [Delete Status]='No' and Id='"+id_get+"'",conn)
        df_course = df_course.rename({'Course Name': 'CourseName', 'Actual Price': 'ActualPrice','Offer Price':'OfferPrice',"Course Overview":"CourseOverview","Course Image":"CourseImage"}, axis=1)
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)
        print(type(course_data))
        context = {"course_data":course_data}
        
    return render(request,'courses_view.html',context)

def about(request):
    return render(request,'about.html')



def enroll_course(request):
    if request.method == "POST":
        email = request.POST["email"]
        id_get = request.POST["id"]
        print(id_get)
        print(email)

        df_course = pd.read_sql("select * from [dbo].[CourseDetails] where [Delete Status]='No' and Id='"+id_get+"'",conn)
        df_course = df_course.rename({'Course Name': 'CourseName', 'Actual Price': 'ActualPrice','Offer Price':'OfferPrice',"Course Overview":"CourseOverview","Course Image":"CourseImage"}, axis=1)
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)
        print(type(course_data))
        context = {"course_data":course_data,"id":id_get}
    return render(request,"enroll_course.html",context)



def order_confirm(request):
    context = {}
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        address = request.POST["address"]
        id_get = request.POST["id"]
        order_temp_id = datetime.now().strftime('%Y%m%d%H%M%S')
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        get_amount=pd.read_sql("select *  from [dbo].[CourseDetails] where id="+str(id_get)+"",conn)
        sql = "insert into [dbo].[orders]( course_id , name, email, mobile, address, order_temp_id, updated_date , datetime , payment_id , order_id , amount_paid , delete_status, order_status ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        params = ( id_get , name , email , mobile , address , order_temp_id , current_date , current_date , 'NA', "NA" , "NA" , "No" , "Not Paid" )
        cursor = conn.cursor()
        cursor.execute(sql,params)
        print("Order Details Added Successfully")
        conn.commit()
        print(get_amount)
        amount = get_amount["Offer Price"].iloc[0]
        print(int(amount)*100)
        currency = 'INR'
        amount = int(amount)*100
        razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        print(razorpay_order_id)
        callback_url = '/paymenthandler/'    
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['order_temp_id'] = order_temp_id
        sql_update = "update [dbo].[orders] set order_id='"+str(razorpay_order_id)+"'  , amount_paid ='"+str(amount)+"' where order_temp_id='"+str(order_temp_id)+"'"
        cursor = conn.cursor()
        cursor.execute(sql_update)
        conn.commit()
        print("Order Details Updated Successfully")
        df_course = pd.read_sql("select * from [dbo].[CourseDetails] where [Delete Status]='No' and Id='"+id_get+"'",conn)
        df_course = df_course.rename({'Course Name': 'CourseName', 'Actual Price': 'ActualPrice','Offer Price':'OfferPrice',"Course Overview":"CourseOverview","Course Image":"CourseImage"}, axis=1)
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)
        print(type(course_data))
        context["course_data"] = course_data
        context["id"] = id_get
        

    return render(request,"order_confirm.html",context)


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            # print("OK")
            payment_id = request.POST['razorpay_payment_id']
            razorpay_order_id = request.POST['razorpay_order_id']
            signature = request.POST['razorpay_signature']
            
            print("OK")
            order_data = pd.read_sql("select *  from [dbo].[orders] where order_id='"+str(razorpay_order_id)+"'",conn)
            
            print("OK")

            sql_update = "update [dbo].[orders] set payment_id='"+str(payment_id)+"'  , order_status ='Paid' where order_id='"+str(razorpay_order_id)+"'"
            cursor = conn.cursor()
            cursor.execute(sql_update)
            conn.commit()


            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # print(params_dict)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            
            if result is None:
                print(params_dict)
                amount = 15000 * 100  # Rs. 200
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount) 
                    return render(request, 'paymentsuccess.html',params_dict)

                except:
                    print("Fail Excepi")
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return "Error in Exception"
    else:
       # if other than POST request is made.
        return "Error in POST"


def search(request):
    if request.method=="GET":
        name_get = request.GET["s"]
        df_course = pd.read_sql("select * from [dbo].[CourseDetails] where [Course Name] like '%"+name_get+"%'",conn)
        print(df_course)
        df_course = df_course.rename({'Course Name': 'CourseName', 'Actual Price': 'ActualPrice','Offer Price':'OfferPrice',"Course Overview":"CourseOverview","Course Image":"CourseImage"}, axis=1)
        course_data = df_course.to_json(orient='records')
        course_data = json.loads(course_data)
        print(type(course_data))
        context = {"course_data":course_data}
        
        if df_course.empty:
            context = {"error":"error"}


    return render(request,'search.html',context)






















def test_template(request):
    return render(request,'paymentsuccess.html')


    