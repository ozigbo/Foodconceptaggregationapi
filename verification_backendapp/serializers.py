
from rest_framework import serializers
from .models import User,Warehouse,ReconcileSaleTransactions,User_Warehouse



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','fullname','first_name','email', 'role','last_name','last_login','username']  # Add other fields as needed




class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields ='__all__'


class ReconcileSaleTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReconcileSaleTransactions
        fields ='__all__'


class UserWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Warehouse
        fields = '__all__'

class UserListWarehouseSerializer(serializers.ModelSerializer):

    user_warehouse = UserWarehouseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'role', 'first_name', 'last_name', 'created_at', 'updated_at', 'user_warehouse']

    def to_representation(self, instance):
        # Fetch the related User_Warehouse objects for the current User instance
        user_warehouses = instance.user_warehouse.all()
        # Serialize the User instance
        serialized_data = super().to_representation(instance)

        # Serialize the related User_Warehouse objects
        user_warehouse_data = UserWarehouseSerializer(user_warehouses, many=True).data
        
        # Add the serialized User_Warehouse data to the serialized User data
        serialized_data['user_warehouse'] = user_warehouse_data

        return serialized_data


