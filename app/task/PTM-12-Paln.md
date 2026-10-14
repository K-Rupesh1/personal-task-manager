Step 1: DB design (sqlalchemy) DB Models
Step 2: Models of your request and response (keep in mind Status is pre-defined field -  try to use the enum, sample - To-Do, IN-progress, Completed, Cancelled)
Step 3: Start creating endpoint using prefix also in different file.
Step 4: You have to add your validations once you receive data from the user. 
              What validations -
			i. Data is empty or not
			ii. Date is future or not
			iii. Description should be more than 6 characters
			iv. Status should not be ‘completed’ when they create
Step 5: your actual business logic (user is valid or not, task name can’t be duplicate, limit of tasks can be created each user) [future scope]
Step 6: save to database using sqlalchemy
Step 7: once save is successful then prepare the Response and give to the api
Step 8: make sure you are using Exceptional handling (try and except and finally blocks)
Step 9: unit testing [future scope]