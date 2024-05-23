from django.forms import ModelForm
from .models import Produit, Fournisseur
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Commentaire
class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        fields = "__all__"

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = '__all__' 
        
class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom')
    last_name = forms.CharField(label='Nom')
    email = forms.EmailField(label='Adresse e-mail')
 
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices=[('carte_bancaire', 'Carte bancaire'), ('cash', 'Paiement en espèces')])
    delivery_checkbox = forms.BooleanField(required=False)


class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['auteur', 'contenu']
    from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'content', 'status', 'image']
        
        from django import forms
from .models import Commande
from django import forms
from .models import Commande

class CommandeForm(forms.ModelForm):
    produits = forms.ModelMultipleChoiceField(queryset=Produit.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = Commande
        fields = ['user', 'dateCde', 'totalCde', 'produits']
