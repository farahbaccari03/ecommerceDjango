from django.utils.translation import gettext_lazy as _
from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Produit(models.Model):
    Categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, null=True)
    Fournisseur = models.ForeignKey('Fournisseur', on_delete=models.CASCADE, null=True)
    TYPE_CHOICES=[  ('em','emballé'),
                    ('fr','Frais'),
                    ('cs','Conserve')]
    
    libelle=models.CharField(max_length=100)
    description=models.TextField(default='non définie')
    prix=models.DecimalField(max_digits=10,decimal_places=3,default=0)
    type=models.CharField(max_length=2,choices=TYPE_CHOICES,default='em')
    img =models.ImageField(upload_to='media/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    
    def __str__(self):
        return self.libelle+","+self.description+","+str(self.prix)+","+self.type
    
class Categorie(models.Model):
    TYPE_CHOICES=[
        ('Al','Alimentaire'),
        ('Mb','Meuble'),
        ('Sn','Sanitaire'),
        ('Vs','Vaisselle'),
        ('Vt','Vetement'),
        ('Jx','Jouets'),
        ('Lg','Ligne de Maison'),
        ('Bj','Bijoux'),
        ('Dc','Decor')
        ]
    libelle=models.CharField(default='Al',choices=TYPE_CHOICES,max_length=50)
    def __str__(self):
        return self.libelle
class Fournisseur (models.Model):
    nom=models.CharField(max_length=100,null=True)
    adresse=models.TextField(null=True)
    email=models.EmailField(null=True)
    telephone=models.CharField(max_length=8,null=True)

    def __str__(self):
        return (self.nom+','+self.adresse+','+self.email+','+self.telephone)
class ProduitNC (Produit):
    Duree_garantie=models.CharField(max_length=100)
    def __str__(self):
        return "Objet ProduitNC"+self.Duree_garantie 
class Commande(models.Model):
    dateCde = models.DateField(null=True, default=date.today)
    nom_client = models.CharField(max_length=100,default="")
    adresse_livraison = models.CharField(max_length=200,default="")
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    produits = models.ManyToManyField(Produit, related_name='produits')

    def __str__(self):
        return str(self.dateCde) + ' - ' + str(self.totalCde)

    def get_produits_info(self):
    
        return [(p.libelle, p.prix,p.qte) for p in self.produits.all()]

class Commission(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    garantie = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # Si c'est une création de produit, on calcule la commission
            self.commission = self.prix * 0.1  # par exemple, une commission de 10%
        super().save(*args, **kwargs)

    def __str__(self):
        return "nom : "+self.nom + " description : "+self.description
        

class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name



class Panier(models.Model):
    STATUS_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('livree', 'Livrée'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_attente')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, null=True)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.produit.libelle} x {self.quantite}"

    def total_produit(self):
        return self.produit.prix * self.quantite

    class Meta:
        verbose_name = _("Panier")
        verbose_name_plural = _("Paniers")

class ContenuPanier(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='contenu')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produit.libelle} x {self.quantite} dans le panier de {self.panier.utilisateur.username}"



class Contact(models.Model):
    sn=models.AutoField(primary_key=True)
    name=models.CharField(max_length=128)
    email=models.CharField(max_length=128)
    phone=models.CharField(max_length=20)
    content=models.TextField()


    def __str__(self):
        return self.name


class Message(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.nom
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Commande1(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit)
    date_commande = models.DateTimeField(default=timezone.now)
    # Autres champs de votre modèle

    def total_prix(self):
        return sum([produit.price for produit in self.produits.all()])

