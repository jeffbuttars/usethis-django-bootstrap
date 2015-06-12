from django.views.generic.base import View, TemplateView


class Index(TemplateView):
    template_name = "sample_index.html"


class Bases(TemplateView):
    template_name = "sample_bases.html"


class BasesStarter(TemplateView):
    template_name = "sample_bases_starter.html"


class BasesJumbotron(TemplateView):
    template_name = "sample_bases_jumbotron.html"
