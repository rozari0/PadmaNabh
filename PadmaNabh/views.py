from django.shortcuts import render
from PadmaNabh.utils import get_cached_data
from django.http import HttpResponse

data = {}


def courseview(request, slug):
    try:
        if data.get(slug):
            context = data.get(slug)
        else:
            context = get_cached_data(slug)[0].get('data')
            print(context)
            data[slug] = context
    except Exception as e:
        print(e)
        return HttpResponse("Die, It's Not Valid.")
    return render(request, template_name="course.html", context={"data": context})


def moduleview(request, slug, module):
    context = get_cached_data(slug)[0].get('data').get('modules').get(module)
    return render(request, template_name="module.html",context={'modules':context})