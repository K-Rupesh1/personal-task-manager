Step 1: DB design by using (sqlalchemy and alembic) DB Models for Register,Login,Password-Reset.
Step 2: Create Models for your request and response,Test Requests and Responses by Using Postman. 
Step 3: Start creating endpoint using prefix and tags (for easy identification), also in different file.
Step 4: Add validations once receive data from the user (for testing use Postman Response). 
              What validations -
			i. Data is empty or not
            ii. Email must have @,.com
            iii. Password must have one uppercase,onelowercase,number and one special character.
Step 5: your actual business logic (user is valid or not, task name can’t be duplicate, limit of tasks can be created each user) [future scope]
Step 6: save to database using sqlalchemy and also alembic
Step 7: once save is successful then prepare the Response and give to the api
Step 8: make sure you are using Exceptional handling (try and except and finally blocks)
Step 9: unit testing [future scope]