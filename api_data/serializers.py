from rest_framework import serializers
from api_data.models import Laptop, LaptopId


class LaptopSerializers(serializers.ModelSerializer):

    class Meta:
        model = Laptop
        fields = '__all__'
        extra_kwargs = {
            'id': { 'required': False }
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('link'):
            ret.update(shop=ret.get('link').split('/')[2])
        else:
            ret.update(shop='')
        return ret

