from django.utils.translation import ugettext_lazy as _

from casia.core.serializers import BooleanFieldSerializer


class YesNoBooleanFieldSerializer(BooleanFieldSerializer):
    TRUE = _('yes')
    FALSE = _('no')
