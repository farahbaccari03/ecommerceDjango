
from django.shortcuts import redirect,get_object_or_404
from django.http import  HttpResponse, HttpResponseRedirect
from .models import Produit
from .models import Fournisseur
from .models import Commande
from .models import Categorie
from .models import Commission
from .models import Panier
from .models import Message
from django.shortcuts import render
from django.template import loader
from .forms import FournisseurForm, ProduitForm ,UserRegistrationForm,UserCreationForm,CommandeForm,AjouterPanierForm,CategorieForm,MessageForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse_lazy
from django.db.models import Q
from rest_framework.views import APIView

from magasin.models import Categorie
from magasin.models import Produit
from magasin.serializers import ProduitSerializer


from rest_framework.response import Response
from magasin.models import Produit
from rest_framework import viewsets
from magasin.models import Categorie
from .serializers import CategorySerializer


from .models import Contact



from django.contrib.auth.decorators import login_required


from .models import Categorie



@login_required
def home(request):
    context={'val':"Menu Acceuil"}
    return render (request,'magasin/acceuil.html',context)
def indexA(request):
    return render(request,'magasin/acceuil.html' )
'''def indexD(request):
    if request.user.is_authenticated:
        request.session['username'] = request.user.username
    return render(request, 'magasin/base.html')'''


def index(request):
       if request.method == "POST" :
         form = ProduitForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Produit.objects.all()
              return render(request,'magasin/vitrine.html',{'list':list})
       else : 
            form = ProduitForm() #créer formulaire vide 
            list=Produit.objects.all()
            return render(request,'magasin/majProduits.html',{'form':form,'list':list})
def indexF(request):
    fournisseurs = Fournisseur.objects.all()
    context = {'fournisseurs': fournisseurs}
    return render(request, 'magasin/mesFournisseurs.html', context)
def nouveauFournisseur(request):
    if request.method == "POST" :
         form = FournisseurForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              nouvFournisseur=Fournisseur.objects.all()
              return render(request,'magasin/vitrineF.html',{'nouvFournisseur':nouvFournisseur})
    else : 
            form = FournisseurForm() #créer formulaire vide 
            nouvFournisseur=Fournisseur.objects.all()
            return render(request,'magasin/fournisseur.html',{'form':form,'nouvFournisseur':nouvFournisseur})
def Catalogue(request):
        products= Produit.objects.all()
        context={'products':products}
        return render( request,'magasin/mesProduits.html',context )
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Produit
from .forms import ProduitForm

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = 'magasin/edit_product.html'
    success_url = reverse_lazy('Catalogue')

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'magasin/delete_product.html'
    success_url = reverse_lazy('Catalogue')


def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f'Coucou {username}, Votre compte a été créé avec succès !')
            return render( request,'magasin/base.html' )
    else :
        form = UserCreationForm()
    return render(request,'magasin/registration/register.html',{'form' : form})
    
    
def liste_commandes(request):
    commandes = Commande.objects.all()
    return render(request, 'magasin/liste_commandes.html', {'commandes': commandes})
def liste_categories(request):
    categories = Categorie.objects.all()
    return render(request, 'magasin/liste_categories.html', {'categories': categories})

def modifier_fournisseur(request, id):
          fournisseur = Fournisseur.objects.get( id=id)
          if request.method == 'POST':
             form = FournisseurForm(request.POST, request.FILES, instance=fournisseur)
             if form.is_valid():
                form.save()
                return redirect('Fournisseur')
          else:
             form = FournisseurForm(instance=fournisseur)
          return render(request, 'magasin/edit_fournisseur.html',{'form': form})

def supprimer_fournisseur(request, id):
     fournisseur = Fournisseur.objects.get( id=id)
     if request.method == 'POST':
        fournisseur.delete()
        return redirect('Fournisseur')
     return render(request, 'magasin/delete_fournisseur.html', {'fournisseur': fournisseur})
     
def liste_Commission(request):
    if request.method == "POST" :
         form = CommissionForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Commission.objects.all()
              return render(request,'magasin/vitrineC.html',{'list':list})
    else : 
            form = CommissionForm() #créer formulaire vide 
            list=Commission.objects.all()
            return render(request,'magasin/liste_Commission.html',{'form':form,'list':list})

def indexCO(request):
       if request.method == "POST" :
         form = CommandeForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              list=Commande.objects.all()
              return render(request,'magasin/vitrineCO.html',{'list':list})
       else : 
            form = CommandeForm() #créer formulaire vide 
            list=Commande.objects.all()
            return render(request,'magasin/majProduits.html',{'form':form,'list':list})



class CategoryAPIView(APIView):
 
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ProduitAPIView(APIView):
 
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)
'''class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitSerializer

  def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset'''
from rest_framework import viewsets
class ProductViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProduitSerializer
    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset





def send_feedback_view(request):
    feedbackForm=forms.FeedbackForm()
    if request.method == 'POST':
        feedbackForm = forms.FeedbackForm(request.POST)
        if feedbackForm.is_valid():
            feedbackForm.save()
            return render(request, 'magasin/feedback_sent.html')
    return render(request, 'magasin/send_feedback.html', {'feedbackForm':feedbackForm})

# admin view the feedback
@login_required(login_url='Login')
def view_feedback_view(request):
    feedbacks=models.Feedback.objects.all().order_by('-id')
    return render(request,'magasin/view_feedback.html',{'feedbacks':feedbacks})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Produit
from .forms import AjouterPanierForm


def liste_produits(request):
    produits = Produit.objects.all()
    # Ajouter le code pour trier les produits ici
    context = {'produits': produits}
    return render(request, 'panier/liste_produits.html', context)

def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == 'POST':
        form = AjouterPanierForm(request.POST)
        if form.is_valid():
            quantite_demandee = form.cleaned_data['quantite']
            if produit.stock >= quantite_demandee:
                panier = request.session.get('panier', {})
                if produit_id in panier:
                    panier[produit_id]['quantite'] += quantite_demandee
                else:
                    panier[produit_id] = {'quantite': quantite_demandee, 'prix': float(produit.prix)}
                request.session['panier'] = panier
                messages.success(request, f"{produit.libelle} a été ajouté au panier.")
                return redirect('liste_produits')
            else:
                messages.error(request, f"Désolé, il n'y a pas assez de stock pour {produit.libelle}.")
    else:
        form = AjouterPanierForm()
    context = {'produit': produit, 'form': form}
    return render(request, 'panier/ajouter_au_panier.html', context)

def contenu_panier(request):
    panier = request.session.get('panier', {})
    contenu = []
    total = 0
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite = info['quantite']
        prix_unitaire = info['prix']
        prix_total = quantite * prix_unitaire
        contenu.append({'produit': produit, 'quantite': quantite, 'prix_unitaire': prix_unitaire, 'prix_total': prix_total})
        total += prix_total
    context = {'contenu': contenu, 'total': total}
    return render(request, 'panier/contenu_panier.html', context)

def passer_commande(request):
    panier = request.session.get('panier', {})
    if not panier:
        messages.error(request, "Votre panier est vide.")
        return redirect('contenu_panier')
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite_demandee = info['quantite']
        if quantite_demandee > produit.stock:
            messages.error(request, f"Désolé, il n'y a plus assez de stock pour {produit.libelle}.")
            return redirect('contenu_panier')
    for produit_id, info in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        quantite_demandee = info['quantite']
        produit.stock -= quantite_demandee
        produit.save()
    request.session['panier'] = {}
    messages.success(request, "Votre commande a été passée.")
    return redirect('liste_produits')


def vider_panier(request):
    request.session['panier'] = {}
    messages.success(request, "Votre panier a été vidé.")
    return redirect('liste_produits')

from django.shortcuts import render
from .models import Panier

def panier_detail(request):
    panier = Panier.objects.filter(utilisateur=request.user)
    total = 0
    for p in panier:
        total += p.total_produit()
    context = {
        'panier': panier,
        'total': total,
    }
    return render(request, 'panier/panier_detail.html', context)



def liste_paniers(request):
    paniers = Panier.objects.all()
    context = {'paniers': paniers}
    return render(request, 'panier/liste_paniers.html', context)



from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render

from .models import Panier, ContenuPanier
from .models import Panier, ContenuPanier
from .forms import PanierForm, ContenuPanierForm,EditPanierForm

from django.forms import inlineformset_factory
from .models import Panier, ContenuPanier

def edit_panier(request, pk):
    panier = get_object_or_404(Panier, pk=pk)
    ContenuPanierFormset = inlineformset_factory(Panier, ContenuPanier, fields=('produit', 'quantite'), extra=1)

    if request.method == 'POST':
        form = EditPanierForm(request.POST, instance=panier)
        formset = ContenuPanierFormset(request.POST, instance=panier)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('liste_paniers')
    else:
        form = EditPanierForm(instance=panier)
        formset = ContenuPanierFormset(instance=panier)

    context = {'form': form, 'formset': formset, 'panier': panier}
    return render(request, 'panier/edit_panier.html', context)


def create_commande(request):
       if request.method == "POST" :
         form = CommandeForm(request.POST)
         if form.is_valid():
              form.save() 
              commandes=Commande.objects.all()
              
              return render(request,'Commandes/mesCommandes.html',{'commandes':commandes})
       else : 
            form = CommandeForm() #créer formulaire vide 
            commandes=Commande.objects.all()
            return render(request,'Commandes/create_commande.html',{'form':form,'commandes':commandes})

def edit_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('ListCommande')
    else:
        form = CommandeForm(instance=commande)
    return render(request, 'Commandes/edit_commande.html', {'form': form})

def delete_commande(request, pk):
    commande = get_object_or_404(Commande, pk=pk)
    if request.method == 'POST':
        commande.delete()
        return redirect('ListCommande')
    return render(request, 'Commandes/delete_commande.html', {'commande': commande})

def detail_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    context = {'commande': commande}
    return render(request, 'Commandes/detail_commande.html', context)

def ListCommande(request):
        commandes= Commande.objects.all()
        context={'commandes':commandes}
        return render( request,'Commandes/mesCommandes.html',context )
        
def create_categorie(request):
       if request.method == "POST" :
         form = CategorieForm(request.POST)
         if form.is_valid():
              form.save() 
              categories=Categorie.objects.all()
              
              return render(request,'Categories/mesCategories.html',{'categories':categories})
       else : 
            form = CategorieForm() #créer formulaire vide 
            categories=Categorie.objects.all()
            return render(request,'Categories/create_categorie.html',{'form':form,'categories':categories})

def edit_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            categorie.save()
            return redirect('ListCategorie')
    else:
        form = CategorieForm(instance=categorie)
        return render(request, 'Categories/edit_categorie.html', {'form': form})

def delete_categorie(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == 'POST':
        categorie.delete()
        return redirect('ListCategorie')
    return render(request, 'Categories/delete_categorie.html', {'categorie': categorie})

def detail_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, id=categorie_id)
    context = {'categorie': categorie}
    return render(request, 'Categories/detail_categorie.html', context)

def ListCategorie(request):
        categories= Categorie.objects.all()
        context={'categories':categories}
        return render( request,'Categories/mesCategories.html',context )


''''def search(request):
    query = request.GET.get('q')
    if query:
        products = Produit.objects.filter(
            Q(libelle__icontains=query) | Q(description__icontains=query)
        ).distinct()
    else:
        products = []
    context = {'query': query, 'products': products}
    return render(request, 'magasin/search_results.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Produit, pk=product_id)
    context = {'product': product}
    return render(request, 'magasin/detail_product.html', context)'''

'''def cart(request):
    order = ContenuPanier.objects.get(customer_name=request.user.username)
    products = order.ordered_products.all()
    context = {'products': products}
    if products.count() > 3:
        discount = order.total_price() * 0.1
        context['discount'] = discount
        context['total_price'] = order.total_price() - discount
    else:
        context['total_price'] = order.total_price()
    return render(request, 'cart.html', context)'''



def do_search(request):
    products = Produit.objects.filter(libelle__icontains=request.GET['q'])
    return render(request, "magasin/mesProduits.html", {"products": products})

class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Categorie.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class ProduitAPIView(APIView):
    def get(self, *args, **kwargs):
        produits = Produit.objects.all()
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

class ProductViewset(viewsets.ReadOnlyModelViewSet):

    serializer_class = ProduitSerializer

    def get_queryset(self):
        queryset = Produit.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(categorie_id=category_id)
        return queryset

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorySerializer

def contact(request):
    if request.method=='POST':
        print(request.POST)
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        print(name,email,phone,content)
        if len(name)<1 or len(email)<3 or len(phone)<5 or len(content)==0:
            messages.error(request,'Please fill the form correctly')
        else:
            contact=Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Your message has been successfully sent')


    return render(request,'magasin/contact.html')

    
from django.contrib.auth.decorators import login_required

@login_required

def indexU(request):
    if request.user.is_authenticated:
        request.session['username'] = request.user.username
    return render(request, 'magasin/index.html')
def TtMessage(request):
        messages= Message.objects.all()
        context={'messages':messages}
        return render( request,'messages/messages.html',context )

def message(request):
       if request.method == "POST" :
         form = MessageForm(request.POST,request.FILES)
         if form.is_valid():
              form.save() 
              messages=Message.objects.all()
              
              return redirect('indexA')
       else : 
            form = MessageForm() #créer formulaire vide 
            messages=Message.objects.all()
            return render(request,'messages/create_msg.html',{'form':form,'messages':messages})
def delete_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        msg.delete()
        return redirect('TtMessage')
    return render(request, 'messages/delete_msg.html', {'msg': msg})

def detail_message(request, msg_id):
    message = get_object_or_404(Message, id=msg_id)
    context = {'message': message}
    return render(request, 'messages/detail_msg.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        produits = Produit.objects.filter(libelle__icontains=query)
        context = {'query': query, 'produits': produits}
        return render(request, 'magasin/search_results.html', context)
    else:
        return render(request, 'magasin/search_results.html')


def product_detail(request, pk):
    product = get_object_or_404(Produit, pk=pk)
    return render(request, 'magasin/detail_product.html', {'product': product})
from django.contrib.auth import logout  # Importer la fonction de déconnexion

def user_logout(request):
    logout(request)
    # Rediriger l'utilisateur vers une page après la déconnexion
    return redirect('index')
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class ConfirmationCommandeView(TemplateView):
    template_name = 'magasin/confirmation_commande.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Récupérer les détails de la commande depuis votre modèle de commande
        # Par exemple, si vous avez un modèle de commande nommé Commande, vous pouvez faire quelque chose comme ceci :
        context['items'] = Commande.objects.all()  # Remplacez VotreModeleDeCommande par le nom de votre modèle de commande
        context['total'] = 0  # Calculez le total de la commande
        return context
