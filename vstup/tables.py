import django_tables2 as tables
from .models import University, Entrant
from .filters import UniversityFilter


class UniversityTable(tables.Table):
    class Meta:
        model = University
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ("name", 'shortName', 'location')


class UniversityFilterTable(UniversityTable):
    class Meta(UniversityTable.Meta):
        model = University
        template_name = 'django_tables2/bootstrap-responsive.html'
        filterset_class = UniversityFilter


# class UniversityHTMxTable(tables.Table):
#     class Meta:
#         model = University
#         template_name = "vstup/bootstrap_htmx.html"


class EntrantsTable(tables.Table):
    # last_name = tables.Column(verbose_name='Прізвище')
    # name = tables.Column(verbose_name="Ім'я")
    # patronymic = tables.Column(verbose_name='Побатькові')
    # phone = tables.Column(verbose_name='Телефон')
    # email = tables.Column(verbose_name='Email')

    class Meta:
        model = Entrant
        # template_name = 'django_tables2/bootstrap-responsive.html'
        template_name = 'django_tables2/bootstrap.html'
        fields = ("last_name", "name", "patronymic", "phone", "email")

class EntrantsDT(tables.Table):
    class Meta:
        model = Entrant
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ('name', 'last_name')