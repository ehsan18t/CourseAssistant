from base.models import Unread_Counts


def notifications(request):
    user = request.user
    notifications_count = 0
    if not Unread_Counts.objects.filter(user=user).exists():
        Unread_Counts.objects.create(user=user)

    notifications_count = Unread_Counts.objects.filter(user=user)[0].notification
    return {
        'notifications_count': notifications_count
    }