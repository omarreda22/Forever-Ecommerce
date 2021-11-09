from .models import Category
from accounts.models import UserProfile



def category_list(request):
    userr = None
    try:
        userr = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        pass

    return {
        'categories' : Category.objects.all(),
        'userr' : userr,
    }