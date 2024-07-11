from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or request.user and request.user.is_staff)
    

class SendPrivateEmailToCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # البته ادمین تمام پرمیشن ها رو داره. اما تابعی که جواب رو به ما میده دست خودمونه.
        # مثلا این دو خط اول رو گذاشتم و دیدم که به کسی که ادمین هم باشه اجازه
        # دسترسی نمیده. حالا میشه شرط ها شو جا به جا کرد دیگه. صرفا جهت تست بود. وگرنه که درستش اینه
        # که ادمین به همه چی دسترسی داشته باشه.
        # if request.user and request.user.is_staff:
        #     return False
        return bool(request.user and request.user.has_perm('store.send_private_email'))


import copy
print(permissions.DjangoModelPermissions().perms_map['GET'])
class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self) -> None:
        self.perms_map = copy.deepcopy(self.perms_map) # برای این که تو حافظه به یه جا اشاره میکنن و
        # این طوری کلا خرابکاری میشه و برای این که این اتفاق نیفته، یه کپی از اون رو ذخیره میکنیم.
        # نکته مهمی هست. دقت کنم.
        self.perms_map['GET']=['%(app_label)s.view_%(model_name)s']
print(CustomDjangoModelPermissions().perms_map['GET'])
print(permissions.DjangoModelPermissions().perms_map['GET'])
