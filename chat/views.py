from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import get_user_model
from django.shortcuts import Http404
# from app.models import Ass
from app.models import Messages_Assigned
from app.views import is_newuser,is_admin,is_consellor
from chat.models import Thread, Message
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
import random
from app.models import *
def home(request):
    return render(request,'home.html')

@login_required(login_url='customerlogin')
# @user_passes_test(is_newuser)
# @user_passes_test(is_admin)
# @user_passes_test(is_consellor,is_newuser)
def get_All_Users(request):

    current_logged_user=User.objects.get(username=request.user.username)
    group_type=current_logged_user.groups.all()[0].name
    print(group_type)


    if group_type=='CONSELLOR':

        all_users =[]
        print("IS CONSELLOR or G_ADMIN")
        only_assigned = Query.objects.filter(assign=current_logged_user.username)
        assigned_unqiue = Query.objects.values('user').distinct()
        for assigned in assigned_unqiue:
            try:
                x= assigned['user']
                usr= User.objects.get(id=x)
                all_users.append(usr)
            except Exception as e:
                print(e)
        #all_users = User.objects.all().exclude(username=request.user.username)
        print(all_users)
        return render(request, "mychats.html", {'all_users': all_users})

    elif group_type=="NEW_USER":
        print("IS NEW_USER")
        g_admins=User.objects.filter(groups__name='G_ADMIN')
        g_admins_list=[qs for qs in g_admins]
        print(g_admins)
        print(type (g_admins))
        random_admin=random.sample(g_admins_list,1)

        ##new stuff
        all_users = []
        only_assigned = Query.objects.filter(user=current_logged_user)
        assigned_unqiue = Query.objects.values('assign').distinct()
        for assigned in assigned_unqiue:

            try:
                x = assigned['assign']
                usr = User.objects.get(username=x)
                all_users.append(usr)
            except Exception as e:
                print(e)
        ##end new stuff

        print(random_admin)

        if Message.objects.filter(sender=current_logged_user).count()==0:
            return render(request, "mychats.html", {"all_users": all_users})

        else:
            all_msg_by_user = Message.objects.filter(sender=current_logged_user)

            temp = []
            for data in all_msg_by_user:
                try:
                    msg = Messages_Assigned.objects.get(Message_Id=data)
                    temp.append(msg.Assigned_To)
                    all_users.append(msg.Assigned_To)

                except Messages_Assigned.DoesNotExist:
                    pass

            return render(request, "mychats.html", {"all_users": all_users})





class ThreadView(View):
    template_name = 'chat/chat.html'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        print("___________________________")
        self.other_user = get_user_model().objects.get(username=other_username)
        obj = Thread.objects.get_or_create_personal_thread(self.request.user, self.other_user)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = {}
        context['me'] = self.request.user
        context['thread'] = self.get_object()
        context['user'] = self.other_user
        context['messages'] = self.get_object().message_set.all()

        current_logged_user = User.objects.get(username=self.request.user.username)
        group_type = current_logged_user.groups.all()[0].name
        print(group_type)

        if group_type == 'CONSELLOR' or group_type == "G_ADMIN":

            print("IS CONSELLOR or GADMIN")
            # all_users = User.objects.all().exclude(username=self.request.user.username)
            # print(all_users)
            msg_assigned_users = Messages_Assigned.objects.filter(Assigned_To=current_logged_user)
            all_users = [users.Message_Id.sender for users in msg_assigned_users]



            context['all_users'] = all_users
            # return render(self.request, "mychats.html", {'all_users': all_users})

        elif group_type == "NEW_USER":
            print("IS NEW_USER")
            g_admins = User.objects.filter(groups__name='CONSELLOR')
            g_admins_list = [qs for qs in g_admins]
            print(g_admins)
            print(type(g_admins))
            random_admin = random.sample(g_admins_list, 1)

            print(random_admin)

            all_msg_by_user=Message.objects.filter(sender=current_logged_user)

            temp=[]
            for data in all_msg_by_user:
                try:
                    msg=Messages_Assigned.objects.get(Message_Id=data)
                    temp.append(msg.Assigned_To)
                except Messages_Assigned.DoesNotExist:
                    pass

            context['all_users'] = temp
            # return render(request, "chat/chat.html", {"all_users": random_admin})




        # context['all_users'] = User.objects.all().exclude(username=self.request.user.username)
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)


    def post(self, request, **kwargs):
        self.object = self.get_object()
        thread = self.get_object()
        data = request.POST
        user = request.user
        text = data.get("message")
        Message.objects.create(sender=user, thread=thread, text=text)
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context=context)


# @method_decorator(csrf_exempt,name="dispatch")
# def fetchUsers(request):
#     uname=request.POST.get('username')
#     print(uname)
#     all_users=User.objects.all().exclude(username=uname)
#     users_list=[]
#     for data in all_users:
#         users_list.append(data.username)
#     print(users_list)
#     return JsonResponse({'result':users_list})
