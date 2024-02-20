#  Copyright (c) $today.year.Leonard Stegle
#  All rights reserved
#  Alle Rechte vorbehalten

from django import forms
from .models import *

# Formulare

# Bewertungsformular
class BewertungForm(forms.ModelForm):
    class Meta:
        # Verknüpfe das Formular mit dem Bewertungsmodell
        model = Bewertung
        # Definiere die Felder, die im Formular angezeigt werden
        fields = ["rating", "identifiziert"]