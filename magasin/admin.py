
from django.contrib import admin
from .models import Produit, Categorie
from .models import Fournisseur
from .models import ProduitNC
from .models import Commande
from .models import Post
from .models import Commentaire
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Fournisseur)
admin.site.register(ProduitNC)
admin.site.register(Commande)
admin.site.register(Post)
admin.site.register(Commentaire)

