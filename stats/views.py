from django.shortcuts import render


def stats(request):
    data = {
        '1': {'id': 1, 'name': 'Semester 1', 'start_date': '2014-01-01', 'end_date': '2014-05-01', 'is_running': False, 'auto_add_to_group': True},
        '2': {'id': 2, 'name': 'Semester 2', 'start_date': '2014-06-01', 'end_date': '2014-12-01', 'is_running': True, 'auto_add_to_group': True},
    }
    return render(request, 'stats/stats.html', {'data': data})
