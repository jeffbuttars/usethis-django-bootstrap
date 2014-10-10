from django.views.generic.base import View, TemplateView


class Index(TemplateView):
    template_name = "sample_index.html"
# Index


# class Login(View):
#     def get(self, req):

#         return render(
#             req,
#             'sample_login.html', 
#             {
#                 'login_form': BSAuthenticationForm,
#             }
#         )
