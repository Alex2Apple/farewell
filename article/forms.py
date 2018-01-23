from django import forms

from accessor.models import Accessor

class CommentForm(forms.Form):
    article_id = forms.IntegerField()
    comment_parent_id = forms.IntegerField()
    email = forms.CharField(max_length = 30)
    username = forms.CharField(max_length = 30)
    website = forms.CharField(max_length = 40, required = False)
    comment = forms.CharField(max_length = 1000)
    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        email_obj = Accessor.objects.filter(email = email)
        if email_obj.exists() == False:
            name_obj = Accessor.objects.filter(name = username)
            if name_obj.exists() == True:
                raise forms.ValidationError("昵称%s已被注册, 更换一个喽" % username)
            Accessor.create_accessor(email, username, cleaned_data.get("website"))
        else:
            obj = email_obj[0]
            obj.name = username
            obj.website = cleaned_data.get("website")
            obj.save()
        return cleaned_data