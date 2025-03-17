**Crypto Data Organisation**
This project is a Celery-based task queue integrated with Redis as the message broker, built using Django. It focuses on managing organizations and periodically updating cryptocurrency prices, such as Bitcoin and Ethereum, for each organization. The periodic updates are handled by Celery, ensuring automated price updates at regular intervals.

**Database Overview**
The project is connected to a MySQL database, which consists of the following key tables:
User Table: Stores user details using Django’s built-in authentication model.
Organization Table: Manages organizational data with CRUD (Create, Read, Update, Delete) operations.
Crypto Price Table: Stores cryptocurrency price data for each organization.

**API Overview**
The project utilizes Django's authentication system to manage user registrations and logins.
A CRUD API is implemented for managing organization data.
A List API is provided to retrieve cryptocurrency prices for a given organization.

**Celery Integration**
Celery is a task queue that enables running background tasks asynchronously in Python. In this project, Celery is used to periodically fetch cryptocurrency prices from a third-party API. This scheduled task executes every five minutes using Celery Beat.

**Redis as a Message Broker**
Redis serves as the message broker for Celery, temporarily storing pending background tasks before they are executed by workers.

**Steps to Run the Project**
1) Install Redis Download and install Redis from the official GitHub repository based on your operating system.
Start Redis Server Run Redis in the background using the redis-cli command.
2) Start the Django Server to Run the Django development server to access the APIs.
3) Run Celery Worker to Start the Celery worker process to fetch cryptocurrency prices:
**celery -A project.celery worker --pool=solo -l info**
4) Start Celery Beat to schedule periodic tasks:
**celery -A project beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler**


