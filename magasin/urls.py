
from django.urls import  path
from . import views
from django.contrib.auth import views as auth_views
from .views import CategoryAPIView
from .views import ProduitAPIView, SelectProduitAPIView
from magasin.views import  CategoryAPIView
from .views import ProductDetailAPIView
from .views import generate_pdf
from django.urls import path

app_name = 'magasin'

urlpatterns = [
    # Autres patterns d'URL...
    path('delete_order/', views.delete_order, name='delete_order'),
    path('generate_pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
 path('creer_commande/', views.creer_commande, name='creer_commande'),
    path('api/produit/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
   path('api/categories/', CategoryAPIView.as_view()),
    path('api/produits/', ProduitAPIView.as_view()),
    path('api/produits/<int:pk>/', SelectProduitAPIView.as_view()),
    path('', views.index, name='index'),
    path('fournisseur/', views.fournisseur, name='fournisseur'),
    path('mesProduits/', views.mesProduits, name='mesProduits'),
    path('add_produit/', views.add_produit, name='add_produit'),
    path('editer-produit/<int:produit_id>/', views.editer_produit, name='editer_produit'),
    path('supprimer-produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
    path('shoppingcart/', views.shoppingcart, name='shoppingcart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    
    path('my_orders/', views.my_orders, name='my_orders'),
    path('add_fournisseur/', views.add_fournisseur, name='add_fournisseur'),
    path('edit/<int:fournisseur_id>/', views.edit_fournisseur, name='edit_fournisseur'),
    path('delete/<int:fournisseur_id>/', views.delete_fournisseur, name='delete_fournisseur'),
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('create_post/', views.create_or_update_post, name='create_post'),
    path('post_update/<int:pk>/', views.create_or_update_post, name='update_post'),
    path('post_delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('liste_commentaires/', views.liste_commentaires, name='liste_commentaires'),
    path('ajouter_commentaire/', views.ajouter_commentaire, name='ajouter_commentaire'),
     path('supprimer_commentaire/<int:commentaire_id>/', views.supprimer_commentaire, name='supprimer_commentaire'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
 
   
]
