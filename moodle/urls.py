"""cso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, re_path
from moodle import views

# APIview
# urlpatterns = [
#
# # ▼ --------------------------------------- ▼  user_urls  ▼ --------------------------------------- ▼
#
#     path('auth/<str:m_ac>',views.EmailAuth.as_view()),  #Email验证
#
#     path('m_users',views.MoodleUsersMsg.as_view()),  #查看所有用户/用户注册
#     path('m_login',views.Login.as_view()),  #用户登录
#     path('m_user',views.MoodleUserMsg.as_view()),  #查看/修改自己
#     path('m_user/<str:pk>',views.MoodleUserMsg.as_view()),  #查看/修改指定用户
#
# # ▲ --------------------------------------- ▲  user_urls  ▲ --------------------------------------- ▲
# # ▼ --------------------------------------- ▼ course_urls ▼ --------------------------------------- ▼
#
#     path('learn_data/<str:judge>',views.MoodleLearnData.as_view()),  #修改用户学习数据
#
#     path('m_courses',views.MoodleCoursesMsg.as_view()),  #查看所有课程(学科)
#     path('m_course',views.MoodleCourseMsg.as_view()),  #查看自己的课程
#     path('m_course/<str:pk>',views.MoodleCourseMsg.as_view()),  #查看指定用户的课程
#
# # ▲ --------------------------------------- ▲ course_urls ▲ --------------------------------------- ▲
#
#     path('sb',views.SB.as_view())
# ]


urlpatterns = [

    path('login', views.Login.as_view(), name='login'),
    path('user', views.User.as_view(), name='user'),
    path('contact', views.Contact.as_view()),

    # 学分认证
    path('credits', views.Credits.as_view()),

    # 我的课程
    path('course', views.Course.as_view(), name='course'),

    # 首页
    path('index', views.Index.as_view(), name='index'),

    # 教授显示某课学生批改作业列表
    path('correct/<str:course_id>/<str:exam_name>', views.Correct.as_view(), name='correct'),

    path('marking/<str:course_id>/<str:exam_id>', views.Marking.as_view(), name='marking'),

    # 教授显示所教的课程
    path('score', views.Score.as_view()),

    # 教授显示所教的课程的全部学生的全部考试成绩
    path('score/<str:course_id>/', views.ShowScore.as_view(), name='score'),


    path('course/<str:course_id>', views.Player.as_view()),
    path('exam/<str:course_id>/<str:exam_name>', views.Exam.as_view(), name='exam'),

    #教授上传pdf
    path('excel',views.Excel.as_view())

]
