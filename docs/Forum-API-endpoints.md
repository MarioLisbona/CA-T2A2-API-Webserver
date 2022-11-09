# **Tables of contents**
- [**Admin routes**](#admin-routes)
- [**Auth routes**](#auth-routes)
- [**User routes**](#user-routes)
- [**Post routes**](#post-routes)
- [**CLI Commands**](#cli-commands)

# **Forum API endpoint documenation**

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

- Response Body: No deactivated posts
  
```JSON
{
    "error": "404 Not Found: There are no deactivated posts in the forum"
}
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

- Response Body: No replies
  
```JSON
{
    "error": "404 Not Found: There are no replies in the forum"
}
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

- Response Body: User has posted No replies
  
```JSON
{
    "error": "404 Not Found: User 1 has not posted any replies"
}
```

- Response Body: User does not exist
  
```JSON
{
    "error": "404 Not Found: User id:12 does not exist"
}
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

  - User does not exist
  
```JSON
{
    "error": "404 Not Found: User id:33 does not exist"
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

  - Post does not exist
  
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

  - User warning attribute greater than or equal to 3 warnings:
  
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


### /admin/users/\<int:user_id\>/grant_admin/

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


### /admin/users/\<int:user_id\>/revoke_admin/

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

[**Back to Table of Contents**](#tables-of-contents)
<hr>
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
[**Back to Table of Contents**](#tables-of-contents)
<hr>
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

[**Back to Table of Contents**](#tables-of-contents)
<hr>
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
- Request Body: 

```JSON
{
    "title": "Europe for Winter",
    "content": "My trip to Europe was amazing. We rode some amazing resorts, found some amazing backcountry terrain and got alot of powder turns in. And the food was unreal!",
    "channel": "Travel"
}
```
- Response Body:
- successfully post to forum:

```JSON
{
    "message": "You successfully added the post to the forum",
    "post details": {
        "id": 13,
        "title": "Europe for Winter",
        "date": "2022-11-08",
        "time": "15:02:08",
        "is_active": true,
        "content": "My trip to Europe was amazing. We rode some amazing resorts, found some amazing backcountry terrain and got alot of pwder turns in. And the food was unreal!",
        "channel": "Travel",
        "user": {
            "f_name": "Mario",
            "l_name": "Lisbona",
            "email": "mario.lisbona@gmail.com"
        },
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

- Example of validation

```JSON
{
    "error": {
        "content": [
            "Length must be between 100 and 2000."
        ],
        "channel": [
            "Must be one of: Travel, Tech, Snowboarding, Surfing, Foiling, Food, Pets, Music"
        ]
    }
}
```

<hr>
<br>


### /posts/\<int:post_id\>/delete/

- Methods: DELETE
- Arguments: *post_id*
- Description: Delete a post that a user owns
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:
- Successful Delete

```JSON
{
    "message": "Post deleted successfully",
    "post id": 13,
    "post Title": "Europe for Winter"
}
```

- Not the owner of the post or an admin

```JSON
{
    "error": "401 Unauthorized: You are not the owner of this post"
}
```

- post does not exist

```JSON
{
    "error": "404 Not Found: Post 3 does not exist"
}
```

<hr>
<br>


### /posts/

- Methods: GET
- Arguments: *None*
- Description: read all active posts
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 12,
        "title": "Europe for Winter",
        "date": "2022-11-08",
        "time": "14:56:44",
        "is_active": true,
        "content": "My trip to Europe was amazing. We rode some amazing resorts, found some amazing backcountry terrain and got alot of pwder turns in. And the food was unreal!",
        "channel": "Travel",
        "user": {
            "f_name": "Mario",
            "l_name": "Lisbona",
            "email": "mario.lisbona@gmail.com"
        },
        "replies": []
    }
]
```

- No active posts in the forum

```JSON
{
    "error": "404 Not Found: There are no active posts in the forum"
}
```

<hr>
<br>



### /posts/\<int:post_id\>/

- Methods: GET
- Arguments: *post_id*
- Description: read a specific post given a post id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:
- Post exists:

```JSON
{
    "id": 12,
    "title": "Europe for Winter",
    "date": "2022-11-08",
    "time": "14:56:44",
    "is_active": true,
    "content": "My trip to Europe was amazing. We rode some amazing resorts, found some amazing backcountry terrain and got alot of pwder turns in. And the food was unreal!",
    "channel": "Travel",
    "user": {
        "f_name": "Mario",
        "l_name": "Lisbona",
        "email": "mario.lisbona@gmail.com"
    },
    "replies": []
}
```
- Post does not exist:
  
```JSON
{
    "error": "404 Not Found: Post 124 does not exist"
}
```

<hr>
<br>



### /posts/users/\<int:user_id\>/

- Methods: GET
- Arguments: *user_id*
- Description: read all posts from a speciifc user given a user id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:
- User exists and has posted to the forum:

```JSON
{
    "msg": "User:1 has posted the following posts to the forum",
    "post details": [
        {
            "id": 1,
            "title": "Traveling to Indonesia",
            "date": "2022-11-07",
            "time": "09:31:11",
            "is_active": false,
            "content": "Post content",
            "channel": "Travel",
            "user": {
                "f_name": "Administrator",
                "l_name": "Admin",
                "email": "admin@forum.com"
            }
        }
    ]
}
```

- User exists and has not posted to the forum:

```JSON
{
    "error": "404 Not Found: The user id:5 - Mario Lisbona has not posted anything to the forum"
}
```

- User does not exist:

```JSON
{
    "error": "404 Not Found: User id 96 does not exist"
}
```

<hr>
<br>



### /posts/\<int:post_id\>/

- Methods: PUT, PATCH
- Arguments: *post_id*
- Description: update a post as the owner
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: Every field can be updated but all fields when updating are also optional. all fields available are shown below

```JSON
{
    "title": "Changing the title of a post!",
    "content": "This will have to be more than 2000 This will have to be more than 2000 chars"
}
```

- Response Body:
- successfully updated post

```JSON
{
    "message": "You successfully updated the post.",
    "post details": {
        "id": 5,
        "title": "Changing the title of a post!",
        "date": "2022-11-08",
        "time": "15:47:16",
        "is_active": true,
        "content": "This will have to be more than 2000 chars",
        "channel": "Tech",
        "user": {
            "f_name": "Mario",
            "l_name": "Lisbona",
            "email": "mario.lisbona@gmail.com"
        },
        "replies": [
            {
                "id": 4,
                "reply": "I am also learning how to use Python with Flask to develop web applications.",
                "date": "2022-11-08",
                "time": "15:43:03",
                "user": {
                    "f_name": "Ali",
                    "l_name": "Taubner",
                    "email": "ali.taubner@gmail.com"
                }
            }
        ]
    }
}
```

- not the owner of the post:

```JSON
{
    "error": "401 Unauthorized: You are not the owner of this post"
}
```

- post does not exist:

```JSON
{
    "error": "404 Not Found: Post 55 does not exist"
}
```


<hr>
<br>


### /posts/\<int:post_id\>/reply

- Methods: POST
- Arguments: *post_id*
- Description: create a reply to a post
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body:
  
```JSON
{
    "reply": "Yes! i love indo!!!! Im heading to the ments in March! :D"
}
```

- Response Body: 

```JSON
{
    "message": "You successfully replied to the post",
    "post title": "Traveling to Indonesia",
    "reply details": {
        "id": 7,
        "reply": "Yes! i love indo!!!! Im heading to the ments in March! :D",
        "date": "2022-11-08",
        "time": "16:02:37"
    }
}
```

- post does not exist:

```JSON
{
    "error": "404 Not Found: Post 55 does not exist"
}
```


<hr>
<br>


### /posts/replies/\<int:reply_id\>/update/

- Methods: POST
- Arguments: *reply_id*
- Description: update a reply to a post as the owner of the reply
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body:
  
```JSON
{
    "reply": "Updating the reply to a post as the owner of the reply"
}
```

- Response Body:
- Successfully update reply

```JSON
{
    "message": "You successfully updated the reply.",
    "reply details": {
        "id": 6,
        "reply": "Updating the reply to a post as the owner of the reply",
        "date": "2022-11-08",
        "time": "16:00:43"
    }
}
```

- Not the owner of the reply

```JSON
{
    "message": "You are not the owner of this Reply"
}
```

- reply does not exist:

```JSON
{
    "error": "404 Not Found: reply 55 does not exist"
}
```

<hr>
<br>

### /posts/replies/\<int:reply_id\>/delete/

- Methods: DELETE
- Arguments: *reply_id*
- Description: Delete a reply to a post as the owner of the reply
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:
- Successfully Delete reply

```JSON
{
    "message": "Reply deleted successfully",
    "reply id": 6,
    "reply": "Updating the reply to a post as the owner of the reply"
}
```

- Not the owner of the reply

```JSON
{
    "error": "401 Unauthorized: You are not the owner of this reply"
}
```

- reply does not exist:

```JSON
{
    "error": "404 Not Found: reply 55 does not exist"
}
```

<hr>
<br>

### /posts/replies/\<int:post_id\>/replies/

- Methods: GET
- Arguments: *post_id*
- Description: display all replies to a post given a post id
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:

```JSON
{
    "message": "View replies on a post",
    "replies": 2,
    "Post information": {
        "id": 5,
        "title": "Changing the title of a post!"
    },
    "Replies": [
        {
            "id": 4,
            "reply": "I am also learning how to use Python with Flask to develop web applications.",
            "date": "2022-11-08",
            "time": "15:43:03",
            "user": {
                "f_name": "Ali",
                "l_name": "Taubner",
                "email": "ali.taubner@gmail.com"
            }
        },
        {
            "id": 8,
            "reply": "Iv just started to learn Flask and im building a forum API",
            "date": "2022-11-09",
            "time": "08:00:55",
            "user": {
                "f_name": "Mario",
                "l_name": "Lisbona",
                "email": "mario.lisbona@gmail.com"
            }
        }
    ]
}
```

- Post does not exist:

```JSON
{
    "error": "404 Not Found: Post 55 does not exist"
}
```

<hr>
<br>

### /posts/channel/\<string:forum_channel\>/

- Methods: GET
- Arguments: *post_id*
- Description: display all posts in a given forum channel
  - Forum channels: Travel, Tech, Snowboarding, Surfing, Foiling, Food, Pets, Music
- Authentication: @jwt_required()
- Headers-Authorization: Bearer {Token} - get_jwt_identity()
- Request Body: *None*
- Response Body:

```JSON
[
    {
        "id": 4,
        "title": "Using Flask for Web Development",
        "date": "2018-05-17",
        "time": "15:43:03",
        "is_active": true,
        "content": "Learning how to build a web application with Flask and Python, Learning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and PythonLearning how to build a web application with Flask and Python",
        "channel": "Tech",
        "user": {
            "f_name": "Ali",
            "l_name": "Taubner",
            "email": "ali.taubner@gmail.com"
        }
    },
    {
        "id": 5,
        "title": "Changing the title of a post!",
        "date": "2022-11-08",
        "time": "15:47:16",
        "is_active": true,
        "content": "This will have to be more than 100 chars and no more than 2000 ",
        "channel": "Tech",
        "user": {
            "f_name": "Mario",
            "l_name": "Lisbona",
            "email": "mario.lisbona@gmail.com"
        }
    }
]

```

- CHannel does not contain any posts:

```JSON
{
    "msg": "There are currently no posts in the 'Snowboarding channel"
}
```

```
- CHannel does not exist:

```JSON
{
    "error": "404 Not Found: There are no channels named 'Hiking'."
}
```

[**Back to Table of Contents**](#tables-of-contents)
<hr>
<hr>
<hr>
<br>

## CLI Commands

- flask db drop
  - drop all tables in the database
- flask db create
  - create the table structures in the database
- flask db seed
  - seed the tables in the database with sample data

[**Back to Table of Contents**](#tables-of-contents)
<hr>
<hr>
<hr>
<br>