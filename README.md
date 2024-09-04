# Discord Clone
This project is a simplified version of Discord, built using Django Rest Framework (DRF). It serves as a backend for a chat application, providing endpoints for user management, friend interactions, and project-related functionalities.

# Table of Content
1. [Feature](#feature)
2. [Installation](#installation)
3. [Usage](#usage)
4. [API Endpoints](#apiendpoints)

## Feature
- User Management: Register, login, and manage user accounts.
- JWT Authentication: Secure endpoints using JWT tokens.
- Docker Support: Easily deployable with Docker.

## Installation
### Using Docker
1. Clone the repository:
  ```
  git clone https://github.com/Vikuuu/discord-django-clone.git
  cd discord-django-clone
  ```
2. Build the Docker:
  ```
  docker build
  ```
3. Run the Docker:
  ```
  docker-compose up
  ```
4. Create a Superuser (optional):
  ```
  docker-compose run --rm app sh -c "python manage.py createsuperuser"
  ```
5. Stop the Docker:
   ```
   docker-compose down
   ```

## Usage
Once the server is running, you cna access the API at `http://127.0.0.1:8000/`

- User Endpoint: Register user, login user, logout user, etc.

You can explore the API using tools like Postman or Django's built-in browsable API.

## API Endpoints

Here's a list of API Endpoint:
- `POST /api/user/crete/` - Register User
- `POST /api/user/login/` - Login User
- `GET /api/user/me/` - Gets current User
- `POST /api/user/refresh/` - Generate new access token
- `POST /api/user/logout/` - Logout User

- `GET /api/user/profile/<str:username>/` - Get the Profile
- `PATCH /api/user/profile/<str:username>/` - Update user profile

- `POST /api/friend/send/<str:username>/` - Send Friend Request
- `POST /api/friend/accept/<str:username>` - Accept Friend Request


# Tasks
- [x] User Creation
- [x] User Authentication
- [x] User Profile View
- [x] Send Friend Request
- [x] Accept Friend Request
- [ ] Chat with Friend
