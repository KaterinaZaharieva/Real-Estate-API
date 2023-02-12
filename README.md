# Real-Estate-API
Real estate site project for my python course

# Description
-The site has 2 types of users: buyers and agents
-buyers can register to view the posts ask questions to the sellers via the text box below the post rate the post save the post to favorites and give a viewing request
-agents have all the rights of buyers including posting

# Setup 
1. Clone the Project From GitHub
2. Set Up a Virtual Environment in the directory where the project is
3. Run pip install -r requirements.txt
4. Migrate Project to the Database
4.1 python manage.py makemigrations app
4.2 python manage.py migrate
5. Run the Project : python manage.py runserver