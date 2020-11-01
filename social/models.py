from django.contrib.auth import get_user_model
from django.db import models


# Contact model from Django3 By Example Book by Antonio Mele
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    @staticmethod
    def get_contact(user_from_obj, user_to_obj):
        try:
            contact = Contact.objects.get(user_from=user_from_obj, user_to=user_to_obj)
        except Contact.DoesNotExist:
            contact = None

        return contact


# Add the following field to User dynamically
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))