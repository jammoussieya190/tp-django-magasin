from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.db import models
from django.urls import reverse

class Categorie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    telephone = models.CharField(max_length=8)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    TYPE_CHOICES = [
    ('Al', 'Alimentaire'),
    ('Mb', 'Meuble'),
    ('Sn', 'Sanitaire'),
    ('Vs', 'Vaisselle'),
    ('Vt', 'Vêtement'),
    ('Jx', 'Jouets'),
    ('Lg', 'Linge de Maison'),
    ('Bj', 'Bijoux'),
    ('Dc', 'Décor'),
]

    libelle = models.CharField(max_length=100)
    description = models.TextField(default='Non définie')
    prix = models.DecimalField(max_digits=10, decimal_places=3)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    img = models.ImageField(blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.libelle} - {self.type} - {self.prix} DT"

class ProduitNC(Produit):
        duree_garantie = models.CharField(max_length=100)
def __str__(self):
        return f"{self.libelle} - {self.type} - {self.prix} DT - Garantie: {self.duree_garantie}"
    


from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Commande(models.Model):
    user = models.CharField(max_length=100)
    dateCde = models.DateField(null=True, default=date.today)
    produits = models.ManyToManyField('Produit')
    totalCde = models.DecimalField(max_digits=10, decimal_places=3, default=0)  # Champ totalCde avec valeur par défaut

    def calculer_total_cde(self):
        total = 0
        for produit in self.produits.all():
            total += produit.prix
        self.totalCde = total
        self.save()  # Enregistrer la commande après la mise à jour du totalCde


    
class Commentaire(models.Model):
    auteur = models.CharField(max_length=100)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def get_absolute_delete_url(self):
        return reverse('supprimer_commentaire', args=[str(self.id)])
    def __str__(self):
        return self.contenu
    
    from django.db import models
from django.contrib.auth.models import User


STATUS = (
 (0,"Draft"),
 (1,"Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    image=models.ImageField(blank=True)
class Meta:
    ordering = ['-created_on']
    def __str__(self):return self.title
