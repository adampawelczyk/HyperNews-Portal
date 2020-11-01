from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
import json
from django.conf import settings


class MainView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Coming soon")


class NewsView(View):
    def get(self, request, post_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news = json.load(json_file)
        context = {"news": news, "link": post_id}
        return render(request, "news/news.html", context=context)