from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from challenge_api.models import Pet


class ApiTests(APITestCase):
    """Test Class for the PetView - Do Not change this file"""

    fixtures = ['user', 'tokens', 'pet_type', 'pets']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return super().setUp()

    def test_get_all_pets(self):
        """Test the list method on the PetView
            Expects the length of the returned data to equal
            the count of Pet objects in the database
        """
        response = self.client.get("/pets")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Pet.objects.count())

    def test_retrieve_single_pet(self):
        """Tests the retrieve method on PetView
            Expects the data to be a dictionary of the pet object with the correct id
        """
        pet_id = 1
        actual: Pet = Pet.objects.get(pk=pet_id)
        response = self.client.get(f'/pets/{pet_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, 
            {
                'id': actual.id,
                'name': actual.name,
                'age': actual.age,
                'favorite_activity': actual.favorite_activity,
                'user': actual.user_id,
                'type': actual.type_id
            }
        )

    def test_delete_pet(self):
        """Test the delete method on PetView
            Expects the pet to be deleted from the database
        """
        pet_id = 4
        response = self.client.delete(f'/pets/{pet_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Pet.DoesNotExist):
            Pet.objects.get(pk=pet_id)

    def test_create_pet(self):
        """Test the create method on PetView
            Expects the status_code to be 201 and the pet object should be added to the database
        """
        pet_data = {
            "name": "Fred",
            "age": 4,
            "type": 3,
            "favorite_activity": "Swimming"
        }
        response = self.client.post('/pets', pet_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

        new_pet = Pet.objects.get(pk=response.data['id'])
        self.assertEqual(new_pet.name, pet_data['name'])
