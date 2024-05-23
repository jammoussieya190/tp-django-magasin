from django.shortcuts import render, redirect
from .forms import CommandeForm
from .forms import ProduitForm, FournisseurForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Commentaire, Produit, Fournisseur
from django.contrib.auth.forms import UserCreationForm
from .models import Produit
from .models import Commande
from magasin.models import Categorie
from magasin.serializers import CategorySerializer
from magasin.models import Produit  
from magasin.serializers import ProduitSerializer  
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from magasin.models import Categorie, Produit
from rest_framework import viewsets
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from .forms import CommentaireForm, PaymentForm
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from io import BytesIO
from reportlab.platypus import Spacer, Image
from .models import Produit
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .models import Commande, Produit
from .serializers import ProduitSerializer
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Fournisseur 
from django.shortcuts import get_object_or_404, render, redirect


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = Produit.objects.get(pk=pk)
        serializer = ProduitSerializer(product)
        return Response(serializer.data)
class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProduitAPIView(APIView):
    def get(self, request, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

class SelectProduitAPIView(APIView):
    def get(self, request, pk):
        try:
            produit = Produit.objects.get(pk=pk)
            serializer = ProduitSerializer(produit)
            return Response(serializer.data)
        except Produit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
def index(request):
    if request.method == "POST":
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        form = ProduitForm()

    list = Produit.objects.all()
    return render(request, 'magasin/vitrine.html', {'list': list, 'form': form})

def mesProduits(request):
    products = Produit.objects.all()
    return render(request, 'magasin/mesProduits.html', {'products': products})

def generate_pdf(request, pk):
    commande = Commande.objects.get(pk=pk)
    produits = commande.produits.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="commande_{pk}.pdf"'
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph(f"<strong>Numéro de commande:</strong> {commande.id}", styles['Normal']))
    elements.append(Paragraph(f"<strong>Date de commande:</strong> {commande.dateCde}", styles['Normal']))
    elements.append(Paragraph(f"<strong>Total de la commande:</strong> {commande.totalCde}", styles['Normal']))
    elements.append(Paragraph("<strong>Produits:</strong>", styles['Normal']))
    for produit in produits:
        elements.append(Paragraph(f"- {produit}", styles['Normal']))
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response



def shoppingcart(request):
    cart = request.session.get('cart', [])
    products = Produit.objects.filter(pk__in=cart)
    total_price = sum(product.prix for product in products)
    return render(request, 'magasin/shoppingcart.html', {'products': products, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = get_object_or_404(Produit, pk=product_id)
  
    if 'cart' not in request.session:
        request.session['cart'] = []
    request.session['cart'].append(product_id)
    request.session.modified = True
    return redirect('magasin:shoppingcart')


def fournisseur(request):
    if request.method == "POST":
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin/fournisseur/')
    else:
        form = FournisseurForm()
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'magasin/fournisseur.html', {'form': form, 'fournisseurs': fournisseurs})


def add_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('magasin:fournisseur'))
    else:
        form = FournisseurForm()
    return render(request, 'magasin/add_fournisseur.html', {'form': form})



def edit_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect('magasin:fournisseur')
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'magasin/edit_fournisseur.html', {'form': form, 'fournisseur': fournisseur})



def delete_fournisseur(request, fournisseur_id):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_id)
    if request.method == 'POST':
        fournisseur.delete()
        return HttpResponseRedirect(reverse('magasin:fournisseur'))
    return render(request, 'magasin/delete_fournisseur.html', {'fournisseur': fournisseur})


@login_required
def home(request):
    context = {'val': "Menu Acceuil"}
    return render(request, 'vitrine.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
     
        messages.error(request, "Méthode non autorisée.")
        return redirect('home')  

@login_required
def my_orders(request):
    orders = Commande.objects.filter(user=request.user)
    return render(request, 'magasin/my_orders.html', {'orders': orders})



def add_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('magasin:mesProduits'))  # Rediriger vers une page montrant tous les produits
    else:
        form = ProduitForm()
    return render(request, 'magasin/add_produit.html', {'form': form})

def editer_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('magasin:mesProduits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'magasin/editer_produit.html', {'form': form, 'produit': produit})

def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        produit.delete()
        return redirect('magasin:mesProduits')
    return render(request, 'magasin/supprimer_produit.html', {'produit': produit})



def liste_commentaires(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_commentaires')
    else:
        form = CommentaireForm()

    commentaires = Commentaire.objects.all()
    return render(request, 'magasin/liste_commentaires.html', {'form': form, 'commentaires': commentaires})

from .forms import CommentaireForm

def ajouter_commentaire(request):
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/magasin')
    else:
        form = CommentaireForm()
    return render(request, 'magasin/ajouter_commentaire.html', {'form': form})
def supprimer_commentaire(request, commentaire_id):
    if request.method == 'POST':
        commentaire = get_object_or_404(Commentaire, id=commentaire_id)
        commentaire.delete()
        return HttpResponseRedirect(reverse('magasin:liste_commentaires'))
    else:
        pass
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import PostForm 

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'magasin/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'magasin/post_detail.html', {'post': post})

def create_or_update_post(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
        is_update = True
    else:
        post = Post()
        is_update = False

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            if is_update:
                return HttpResponseRedirect(reverse('magasin:post_list'))
            else:
                
                if request.user.is_authenticated:
                     return HttpResponseRedirect(reverse('magasin:post_list'))
                else:
                    
                        return HttpResponseRedirect(reverse('magasin:post_list'))
    else:
        form = PostForm(instance=post)

    return render(request, 'magasin/post_form.html', {'form': form})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('magasin:post_list')


from django.shortcuts import render, redirect
from .models import Commande, Produit
from django.shortcuts import render, redirect
from .models import Commande, Produit

def create_order(request):
    if request.method == 'POST':
        
        nom = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('phone')
        adresse = request.POST.get('address')
        methode_paiement = request.POST.get('payment_method')
        livraison = request.POST.get('delivery_checkbox')
        nouvelle_commande = Commande.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            adresse=adresse,
            methode_paiement=methode_paiement,
            livraison=livraison
        )

        # Récupérer les produits commandés et leurs quantités
        produits = Produit.objects.all()
        for produit in produits:
            quantite = request.POST.get('quantity' + str(produit.id))
            if quantite:
                nouvelle_commande.produits.add(produit, through_defaults={'quantite': quantite})

        # Rediriger vers une page de confirmation ou une autre destination
        return redirect('order_confirmation')  # Remplacez 'order_confirmation' par l'URL appropriée

    else:
        # Si la méthode HTTP n'est pas POST, afficher simplement le formulaire
        produits = Produit.objects.all()
        total_price = sum(produit.prix for produit in produits)
        return render(request, 'nom_de_votre_app/commandes.html', {'products': produits, 'total_price': total_price})

def passer_commande(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('name')
        email = request.POST.get('email')
        telephone = request.POST.get('phone')
        adresse = request.POST.get('address')
        methode_paiement = request.POST.get('payment_method')
        livraison = request.POST.get('delivery_checkbox')

        # Créer une nouvelle commande
        nouvelle_commande = Commande.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            adresse=adresse,
            methode_paiement=methode_paiement,
            livraison=livraison
        )

        # Récupérer les produits commandés et leurs quantités
        produits = Produit.objects.all()
        for produit in produits:
            quantite = request.POST.get('quantity' + str(produit.id))
            if quantite:
                nouvelle_commande.produits.add(produit, through_defaults={'quantite': quantite})
                return redirect('home') 

    else:
        # Si la méthode HTTP n'est pas POST, afficher simplement le formulaire
        produits = Produit.objects.all()
        total_price = sum(produit.prix for produit in produits)
        return render(request, 'magasin/my_orders.html', {'products': produits, 'total_price': total_price})
from django.shortcuts import render
from .models import Commande

def order_confirmation(request):
    last_order = Commande.objects.filter(user=request.user).latest('dateCde')

    return render(request, 'nom_de_votre_app/order_confirmation.html', {'last_order': last_order})

def creer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.save()
            produits = form.cleaned_data['produits']
            commande.produits.set(produits)
            return HttpResponseRedirect(reverse('magasin:ajouter_commentaire'))
    else:
        form = CommandeForm()
    return render(request, 'magasin/creer_commande.html', {'form': form})



def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        if order_id:
            commande = get_object_or_404(Commande, pk=order_id)
            commande.delete()
            return redirect('magasin:my_orders')
        else:
         
            return JsonResponse({'error': 'Identifiant de commande manquant dans les données POST.'}, status=400)
    else:
     
        return JsonResponse({'error': 'La méthode de la requête doit être POST.'}, status=405)

