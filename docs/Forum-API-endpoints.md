# Forum API endpoint documenation

## Admin routes:

### /admin/stats/

- Methods: GET
- Arguments: *None*
- Description: Returns forum statistics
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:

```JSON
{
    "message": "Forum Statistics",
    "channels": 8,
    "active Posts": 3,
    "archived Posts": 2,
    "replies": 5,
    "users": 5,
    "administrators": 1
}
```

<hr>
<br>

### /admin/posts/deactivated/

- Methods: GET
- Arguments: *None*
- Description: Returns all posts that have been deactivated/archived
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token}  - Admin only
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 1,
        "title": "Traveling to Indonesia",
        "date": "2022-11-07",
        "time": "09:31:11",
        "is_active": false,
        "content": "Post Content",
        "channel": "Travel",
        "user": {
            "f_name": "Administrator",
            "l_name": "Admin",
            "email": "admin@forum.com"
        },
        "replies": []
    }
]
```

<hr>
<br>

### /admin/users/

- Methods: GET
- Arguments: *None*
- Description: Returns all user profiles
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token}  - Admin only
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 2,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com",
        "is_admin": false,
        "warnings": 0
    }
]
```

<hr>
<br>


### /admin/replies/

- Methods: GET
- Arguments: *None*
- Description: Returns all user replies posted on the forum
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 3,
        "reply": "That sounds great, id love to learn to code as well, That sounds great, id love to learn to code as well",
        "date": "2022-11-07",
        "time": "09:31:11",
        "user": {
            "f_name": "Ali",
            "l_name": "Taubner",
            "email": "ali.taubner@gmail.com"
        }
    }
]
```

<hr>
<br>


### /admin/users/\<int:reply_user_id\>/replies/

- Methods: GET
- Arguments: *reply_user_id*
- Description: Returns all replies posted by the given user id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 7,
        "reply": "Wow,thats great!!",
        "date": "2022-11-07",
        "time": "11:13:22"
    }
]
```

<hr>
<br>


### /admin/replies/\<int:reply_id\>/delete/

- Methods: DELETE
- Arguments: *reply_id*
- Description: Deletes a reply with the given reply id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successful Delete

```JSON
{
    "message": "Reply deleted successfully",
    "post id": 3,
    "reply": "That sounds great, id love to learn to code as well."
}
```

  - Reply does not exist
  
```JSON
{
    "error": "404 Not Found: Reply 35 does not exist"
}
```
<hr>
<br>


### /admin/users/\<int:user_id\>/

- Methods: GET
- Arguments: *user_id*
- Description: returns the user profile for the given user id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:

```JSON
{
    "id": 3,
    "f_name": "Ali",
    "l_name": "Taubner",
    "email": "ali.taubner@gmail.com",
    "is_admin": false,
    "warnings": 0,
    "posts": [],
    "replies":[]
}
```

<hr>
<br>


### /admin/posts/\<int:post_id\>/delete/

- Methods: DELETE
- Arguments: *post_id*
- Description: Deletes a post with the given post id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successful Delete

```JSON
{
    "message": "Post deleted successfully",
    "post id": 2,
    "post Title": "Traveling to Alaska"
}
```

  - Reply does not exist
  
```JSON
{
    "error": "404 Not Found: Post 22 does not exist"
}
```

<hr>
<br>


### /admin/posts/\<int:post_id\>/deactivate/

- Methods: PATCH
- Arguments: *post_id*
- Description: deactivate a post with the given post id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successful deactivation

```JSON
{
    "message": "You successfully deactivated the post.",
    "post details": {
        "id": 1,
        "title": "Traveling to Indonesia",
        "date": "2022-11-07",
        "time": "09:31:11",
        "is_active": false,
        "content": "Post content.",
        "channel": "Travel",
        "user": {
            "f_name": "Administrator",
            "l_name": "Admin",
            "email": "admin@forum.com"
        },
        "replies": []
    }
}
```

  - Post status is already deactivated

```JSON
{
    "Message": "Post is already deactivated",
    "post details": {
        "id": 1,
        "title": "Traveling to Indonesia",
        "date": "2022-11-07",
        "time": "09:31:11",
        "is_active": false,
        "content": "Post content.",
        "channel": "Travel",
        "user": {
            "f_name": "Administrator",
            "l_name": "Admin",
            "email": "admin@forum.com"
        },
        "replies": []
    }
}
```

  - Post does not exist

```JSON
{
    "error": "404 Not Found: Post id:13 does not exist"
}
```

<hr>
<br>


### /admin/posts/\<int:post_id\>/activate/

- Methods: PATCH
- Arguments: *post_id*
- Description: activate a post with the given post id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successful activation

```JSON
{
    "message": "You successfully activated the post.",
    "post details": {
        "id": 1,
        "title": "Traveling to Indonesia",
        "date": "2022-11-07",
        "time": "09:31:11",
        "is_active": true,
        "content": "Post content.",
        "channel": "Travel",
        "user": {
            "f_name": "Administrator",
            "l_name": "Admin",
            "email": "admin@forum.com"
        },
        "replies": []
    }
}
```

  - Post status is already activated

```JSON
{
    "Message": "Post is already activated",
    "post details": {
        "id": 1,
        "title": "Traveling to Indonesia",
        "date": "2022-11-07",
        "time": "09:31:11",
        "is_active": true,
        "content": "Post content.",
        "channel": "Travel",
        "user": {
            "f_name": "Administrator",
            "l_name": "Admin",
            "email": "admin@forum.com"
        },
        "replies": []
    }
}
```

  - Post does not exist

```JSON
{
    "error": "404 Not Found: Post id:13 does not exist"
}
```

<hr>
<br>


### /admin/users/\<int:user_id\>/issue_warning/

- Methods: PATCH
- Arguments: *user_id*
- Description: Updates a profile - increments the warnings attribute by 1
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- User warning attribute less than 3 warnings:

```JSON
{
    "message": "Warning - User has violated community guidelines",
    "user id": 4,
    "first name": "Coda",
    "last name": "Cat",
    "remaining warnings till banned": 2
}
```

  - User warning attribute greater than 3 warings:

```JSON
{
    "message": "User has been banned from the forum",
    "user id": 4,
    "first name": "Coda",
    "last name": "Cat"
}
```

  - User does not exist

```JSON
{
    "error": "404 Not Found: User id:13 does not exist"
}
```

<hr>
<br>


### /admin/users/\<int:user_id\>/delete/

- Methods: DELETE
- Arguments: *user_id*
- Description: Deletes a user profile - only if user warnings are greater than 3 warnings
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- User warning attribute less than 3 warnings:

```JSON
{
    "message": "User still has warnings remaining, they cannot be banned until 3 warnings have been issued",
    "user id": 3,
    "first name": "Ali",
    "last name": "Taubner",
    "remaining warnings till banned": 3
}
```

  - User warning attribute greater than or equal to 3 warings:
  
```JSON
{
    "message": "User has been successfully banned from the forum",
    "user id": 3,
    "first name": "Ali",
    "last name": "Taubner"
}
```

  - User does not exist

```JSON
{
    "error": "404 Not Found: User id:13 does not exist"
}
```

<hr>
<br>


### users/\<int:user_id\>/grant_admin/

- Methods: PATCH
- Arguments: *user_id*
- Description: Updates a user profile to grant admin rights to the user id given
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successfully grant admin rights:

```JSON
{
    "message": "You successfully granted admin privileges to the user.",
    "updated user details": {
        "id": 2,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com",
        "is_admin": true,
        "warnings": 0
    }
}
```

  - User already has admin rights:

```JSON
{
    "message": "User already has admin privileges",
    "user details": {
        "id": 2,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com",
        "is_admin": true,
        "warnings": 0
    }
}
```

  - User does not exist

```JSON
{
    "error": "404 Not Found: User id:13 does not exist"
}
```

<hr>
<br>


### users/\<int:user_id\>/revoke_admin/

- Methods: PATCH
- Arguments: *user_id*
- Description: Updates a user profile to revoke admin rights to the user id given
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - Admin only
- Request Body: *None*
- Response Body:
- Successfully revoke admin rights:

```JSON
{
    "message": "You successfully revoked admin privileges from the user.",
    "updated user details": {
        "id": 2,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com",
        "is_admin": false,
        "warnings": 0
    }
}
```

  - User already has no admin rights:

```JSON
{
    "message": "User does not have admin privileges",
    "user details": {
        "id": 2,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com",
        "is_admin": false,
        "warnings": 0
    }
}
```

  - User does not exist
  
```JSON
{
    "error": "404 Not Found: User id:13 does not exist"
}
```

<hr>
<hr>
<br>


## Auth routes:

### /auth/register/

- Methods: POST
- Arguments: *None*
- Description: Registers/Create a new user in the database
- Authentication: *None*
- Headers-Authorization: *None*
- Request Body:

```JSON
{
    "f_name": "Mario",
    "l_name": "Lisbona",
    "email": "Mario.Lisbona@geemail.com",
    "password": "1234567Dd!"
}
```

- Response Body:
- Register user successfully

```JSON
{
    "message": "Successfully registered new user to the forum",
    "new user details": {
        "id": 7,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "Mario.Lisbona@geemail.com",
        "is_admin": false,
        "warnings": 0,
        "posts": [],
        "replies": []
    }
}
```

- Email already exists

```JSON
{
    "error": "409 Conflict: Email address 'Mario.Lisbona@geemail.com' already exists"
}
```

<hr>
<br>


### /auth/login/

- Methods: POST
- Arguments: *None*
- Description: Login as a registered user
- Authentication: *None*
- Headers-Authorization: *None*
- Request Body:

```JSON
{
    "email": "Mario.Lisbona@geemail.com",
    "password": "1234567Dd!"
}
```

- Response Body:
- Register logs in successfully

```JSON
{
    "email": "Mario.Lisbona@geemail.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2Nzg3NzU4OSwianRpIjoiNzIyNzNkNzMtMGNmZC00MzkzLTk4ZDktMjE1NWQ2Yzg0MzRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjciLCJuYmYiOjE2Njc4Nzc1ODksImV4cCI6MTY2Nzk2Mzk4OX0.ohKwz3vwpwRBuJX06SqeJm3jq4ZqPU05z-kVYqh8XOU",
    "is_admin": false
}
```

- login unsuccessful

```JSON
{
    "error": "401 Unauthorized: Invalid email or password"
}
```

<hr>
<hr>
<br>


## User routes:

### /users/profile/

- Methods: GET
- Arguments: *None*
- Description: View a user's own profile
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:
- Display user successfully

```JSON
{
    "id": 7,
    "f_name": "Mario",
    "l_name": "Lisbona",
    "email": "Mario.Lisbona@geemail.com",
    "is_admin": false,
    "warnings": 0,
    "posts": [],
    "replies": []
}
```

- Display user unsuccessfully

```JSON
{
    "msg": "Signature verification failed"
}
```

```JSON
{
    "msg": "Token has expired"
}
```

<hr>
<br>


### /users/update_profile/

- Methods: GET
- Arguments: *None*
- Description: Update a user's own profile
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: Every field can be updated but all fields when updating are also optional. 

```JSON
{
    "f_name": "Mario",
    "l_name": "Lisbona",
    "email": "Mario.Lisbona@geemail.com",
    "password": "1234567Dd!"
}
```

- Response Body:
- Request body empty

```JSON
{
    "message": "You made no changes to the user profile.",
    "user details": {
        "id": 7,
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "Mario.Lisbona@geemail.com",
        "is_admin": false,
        "warnings": 0,
        "posts": [],
        "replies": []
    }
}
```

- Profile updated profile successfully with just f_name field

```JSON
{
    "message": "You successfully updated the user's profile.",
    "new user details": {
        "id": 7,
        "f_name": "Muzza",
        "l_name": "Lisbona",
        "email": "Mario.Lisbona@geemail.com",
        "is_admin": false,
        "warnings": 0,
        "posts": [],
        "replies": []
    }
}
```

- Token valid but user has been deleted from database

```JSON
{
    "error": "404 Not Found: User 7 does not exist"
}
```

<hr>
<hr>
<br>


## Post routes:

### /posts/

- Methods: POST
- Arguments: *None*
- Description: Create a post to add to the forum
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: Every field can be updated but all fields when updating are also optional. 

```JSON
{
    "title": "Europe for Winter",
    "content": "My trip to Europe was amazing. We rode some amazing resorts, found some amazing backcountry terrain and got alot of pwder turns in. And the food was unreal!",
    "channel": "Travel"
}
```
