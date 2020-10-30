#### All Actions uses url : : /api/v1/user/

#### 1. Login
- POST
- {
    'username' : __str__,
    'password' : __str__
}

[ Uses CSRF, which is located in the cookies, if not found, do GET method on the given url.]

### 2. Get Current User
- GET
