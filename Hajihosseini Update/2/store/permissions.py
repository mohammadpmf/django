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
