# Django Assessment
This assessment will check your ability to write django models, serializers, and viewsets.

This will also assess your ability to solve problems and ask for help. Use your resources! This includes instructors, google, and past projects. This does not include teammates. 

### Completing the Assessment
1. Set up the virtual environment
    ```sh
    pipenv shell
    pipenv install
    ```

2. In order to pass the assessment, you will need to add code to the `Pet` and `PetType` models, `PetView`, `PetSerializer`, and `urls.py`. Read below for more instructions.
3. There is a test file that will check your work. To run the tests before pushing to github `python3 manage.py test` will show you the test output.
4. Once you are satisfied with your work, push up your code to github.


### Steps

#### 1. Create the ERD
* There will be 3 tables on your ERD, `Pet`, `PetType`, and `User` (will be the django user).
* The `Pet` table should include:
    * name
    * age
    * favorite_activity
* The `PetType` table should include:
    * label
* A `User` can have many pets, but a `Pet` can only have one user
* A `Pet` will have one pet_type

#### 2. Create The Models
* Take your erd and create the `Pet` and `PetType` models
* Update the database to include the new tables
* Run the fixtures: `python3 manage.py loaddata user tokens pet_type pets`

#### 3. PetSerializer
* The serializer should include all the fields on the Pet model
* Any ForeignKey fields should return an integer, not the object

#### 4. Add a `list` method to the PetView
* The list method should return a list of all pets in the database
* The test_get_all_pets test should pass
* To run only this test `python3 manage.py test challenge_api.tests.ApiTests.test_get_all_pets`

#### 5. Add a `retrieve` method to the PetView
* The retrieve method should return a single Pet based on the pk in the url
* If the Pet with that pk is not found, then it should return a 404 response
* The test_retrieve_single_pet test should pass
* To run only this test: `python3 manage.py test challenge_api.tests.ApiTests.test_retrieve_single_pet`

#### 6. Add a `create` method to the PetView
* Assuming an object like this is sent from the client, a Pet object should be added to the dictionary
    ```
    {
        "name": "Fred",
        "age": 4,
        "type": 3,
        "favorite_activity": "Swimming"
    }
    ```
* The status code returned should be a 201
* The new Pet object should be returned in the response
* The test_create_pet test should pass
* To run only this test: `python3 manage.py test challenge_api.tests.ApiTests.test_create_pet`

#### 7. Add a `destroy` method to the PetView
* The delete method should remove the Pet object from the database
* The response status code should be a 204
* The test_delete_pet test should pass
* To run only this test: `python3 manage.py test challenge_api.tests.ApiTests.test_delete_pet`
