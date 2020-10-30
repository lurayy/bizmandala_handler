#### All Actions if not specified uses url : : /api/v1/user/

#### 1. Login
- POST
- {
    'username' : __str__,
    'password' : __str__
}

[ Uses CSRF, which is located in the cookies, if not found, do GET method on the given url.]

### 2. Get Current User
- GET

### 3. Delete User account
- Delete
[Once the user account is delete, only super admin can re-activate it.]

### 4. Update user details
- PATCh
```
{
    'first_name' : __str__/null,
    'last_name' : __str__/null,
    'profile' : {
        'address' : __str__ / null,
        'phone_number' : __str__ / null,
        'phone_number2' : __str__ / null,
        'post' : __str__ / null,
        'profile_image' : __base_64_format / 'None'/ null,
    }
}
```

### 5. Logout
- url : /api/v1/user/logout
- GET

### 6. Register new user
- /api/v1/user/register
- POST
```
{
    'first_name' : __str__,
    'last_name' : __str__,
    'username' : __str__,
    'email' : __str__,
    'password' : __str__,
    'profile' : {
        'address' : __str__ ,
        'phone_number' : __str__ ,
        'phone_number2' : __str__,
        'post' : __str__ ,
        'profile_image' : __base_64_format / 'None'/ null,
    }
}
```

