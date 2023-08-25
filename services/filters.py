import django_filters
from dal import autocomplete
from .choices import *
from django_filters import ChoiceFilter, DateRangeFilter
from django.contrib.auth.models import User
from .models import *
from taggit.models import Tag

class ApplicationFilter(django_filters.FilterSet):
    user = django_filters.ModelChoiceFilter(queryset = User.objects.all(),
    widget=autocomplete.ModelSelect2(
    url='user_autocomplete',
    attrs={
            # Set some placeholder
            # Only trigger autocompletion after 2 characters have been typed
            'data-minimum-input-length': 2,
            'data-width': '100%',
            },
        )
    )
    tags = django_filters.ModelMultipleChoiceFilter(label = "Skills",queryset = Tag.objects.all(),
        widget = autocomplete.ModelSelect2Multiple(url='tags_autocomplete',
            attrs={
            # Set some placeholder
            # Only trigger autocompletion after 2 characters have been typed
            'data-minimum-input-length': 2,
            'data-width': '100%',
            },
        ),
    )
    date_of_application = DateRangeFilter()
    department_preferences = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Application
        fields = ['tags','status','department_preferences','date_of_application',"accepted_department"]