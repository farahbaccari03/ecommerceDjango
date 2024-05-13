from django.forms import ModelForm 
from .models import Produit 
from .models import Fournisseur 
from .models import Commande
from .models import Categorie
from .models import Commission
from .models import Feedback
from .models import Message
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class ProduitForm(ModelForm):
     class Meta : 
        model = Produit
        fields = "__all__" #pour tous les champs de la table
        #fields=['libellé','description']  #pour qulques champs
class FournisseurForm(ModelForm):
     class Meta : 
        model = Fournisseur
        fields = "__all__" #pour tous les champs de la table
        #fields=['libellé','description']  #pour qulques champs
class UserRegistrationForm(UserCreationForm):
      first_name = forms.CharField(label='Prénom')
      last_name = forms.CharField(label='Nom')
      email = forms.EmailField(label='Adresse e-mail')
      class Meta(UserCreationForm.Meta):
         model = User
         fields = UserCreationForm.Meta.fields + ('first_name', 'last_name' , 'email')
class CommandeForm(forms.ModelForm):
    produits = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Commande
        fields = '__all__'
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = "__all__" 
class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['nom', 'description', 'prix', 'garantie']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model= Feedback
        fields=['name','feedback']


from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Panier

class EditPanierForm(forms.ModelForm):
   
    status = forms.ChoiceField(choices=Panier.STATUS_CHOICES)

    class Meta:
        model = Panier
        fields = ['status', 'utilisateur']

class AjouterPanierForm(forms.ModelForm):
    quantite = forms.IntegerField(min_value=1, label=_("Quantité"))


    class Meta:
        model = Panier
        fields = ['quantite']


from django import forms
from django.forms.models import inlineformset_factory
from .models import Panier, ContenuPanier

class PanierForm(forms.ModelForm):
    class Meta:
        model = Panier
        fields = ('status',)

ContenuPanierFormSet = inlineformset_factory(
    Panier, ContenuPanier,
    fields=('produit', 'quantite'),
    extra=0, can_delete=True
)


from django import forms
from django.forms import inlineformset_factory
from .models import Panier, ContenuPanier

class ContenuPanierForm(forms.ModelForm):
    class Meta:
        model = ContenuPanier
        fields = ['produit', 'quantite']

ContenuPanierFormset = inlineformset_factory(Panier, ContenuPanier, form=ContenuPanierForm, extra=1, can_delete=True)
class MessageForm(ModelForm):
     class Meta : 
        model = Message
        fields = "__all__" #pour tous les champs de la table