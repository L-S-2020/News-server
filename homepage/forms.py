#  Copyright (c) $today.year.Leonard Stegle
#  All rights reserved
#  Alle Rechte vorbehalten

from django import forms
from .models import *

class BewertungForm(forms.ModelForm):
    class Meta:
        model = Bewertung
        fields = ["rating", "identifiziert"]