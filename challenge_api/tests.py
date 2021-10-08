from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from challenge_api.models import Pet


class ApiTests(APITestCase):
    """Test Class for the PetView - Do Not change this file"""

    fixtures = ['user', 'pet_type', 'pets']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        token = Token.objects.create(user=self.user)
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
            response.data, {
                'id': actual.id,
                'name': actual.name,
                'age': actual.age,
                'favorite_activity': actual.favorite_activity,
                'user': actual.user_id,
                'type': actual.type_id
            }
        )

    def test_retrieve_returns_404_not_found(self):
        """Tests the retrieve method on PetView
            If an invalid id is used, the retrieve method should return a 404 status code
        """
        response = self.client.get('/pets/100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_pet(self):
        """Tests the update method on PetView
            Expects the pet object to be updated in the database and a 204 status code returned
        """
        pet_id = 2
        og_pet = Pet.objects.get(pk=pet_id)
        update_data = {
            'id': og_pet.id,
            'name': og_pet.name,
            'age': 9,
            'favorite_activity': og_pet.favorite_activity,
            'type': og_pet.type_id
        }
        response = self.client.put(
            f'/pets/{pet_id}', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        updated_pet = Pet.objects.get(pk=2)
        self.assertEqual(updated_pet.age, update_data['age'])

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
            "type_id": 3,
            "favorite_activity": "Swimming"
        }
        response = self.client.post('/pets', pet_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['id'])

        new_pet = Pet.objects.get(pk=response.data['id'])
        self.assertEqual(new_pet.name, pet_data['name'])

    def test_filter_pet_list_by_type(self):
        """Test the list method with a query string parameter
            Expects all the pets in the response.data to have the type requested
        """
        type_id = 2
        response = self.client.get(f'/pets?type={type_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            all([int(pet['type']) == type_id for pet in response.data]))

    def test_my_pets(self):
        """Test the my_pets custom action
            Expects the pets in the response.data to belong to the current user
        """
        response = self.client.get('/pets/my_pets')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all([pet['user'] == self.user.id for pet in response.data]))
