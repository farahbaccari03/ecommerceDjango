

from rest_framework.serializers import ModelSerializer
from .models import Fournisseur,Produit,Categorie

class ProduitSerializer(ModelSerializer):
    class Meta:
        model=Produit
        fields='__all__'

"""class FournisseurSerializer(serializers.ModelSerializer):
    class Meta:
        model=Fournisseur
        fields='_all_'"""

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'libelle']
