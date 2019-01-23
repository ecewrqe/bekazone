from django import forms

class BaseModelForm(forms.ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field = cls.base_fields[field_name]
            attr_dic = {'class': 'form-control'}

            field.widget.attrs.update(attr_dic)
        return forms.ModelForm.__new__(cls)


def create_dynamic_modelform(model_class):
    # to generate many class object

    class Meta:
        model = model_class
        fields = "__all__"

    base_form=type("DynamicForm".encode("utf8"), (BaseModelForm, ), {'Meta':Meta})
    return base_form

