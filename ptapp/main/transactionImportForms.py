from django import forms

from .models import Accounts

###################################################################
# Custom ModelChoiceField that adds a "new" option to the choices
###################################################################
#class ModelChoiceFieldWithNew(forms.ModelChoiceField):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.choices = list(self.choices) + [('0', 'New')]
#
#    def clean(self, value):
#        if(self.required and not value):
#            raise ValidationError(self.error_messages['required'], code='required')
#        if(value == u'0'):
#            return value
#        return super.clean(value)

###################################################
# Class representing the form used for uploading
# lists of transactions for analysis
###################################################
class TransactionFileUploadForm(forms.Form):
    importFile = forms.FileField()

###############################################################
# Class representing the form used for confirming file imports
###############################################################
class ImportConfirmationForm(forms.Form):

    # This field is not required because not answering indicates that it is a new account
    Account = forms.ModelChoiceField(queryset=None, empty_label="New", required=False)

    def __init__(self, *args, **kwargs):
        """
        @param choiceList - List of posible account choices to put in the dropdown
        """
        super().__init__(*args, **kwargs)

        #choiceList.append(('new', "New Account"))
        self.fields['Account'].queryset=Accounts.objects.all()
