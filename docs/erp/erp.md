## ERP APIs
- /api/v1/erps/

#### 1. Get
a. Single
- /api/v1/erps/__uuid__

b. Multiple
- /api/v1/erps/
- Accepeted values : start, lmt, company, address
- example = /api/v1/erps?start=10&lmt=100

#### 2. POST
```
{
    company : __str__,
    address : __str__,
    credit : __credit_id__,
}
```

#### 3. Delete
- /api/v1/erps/__uuid__

#### 4. Patch
- /api/v1/erps/__uuid__
```
{
    address : None/ __str__,
    company : None / __str__
}
```

#### 5. Stop Running ERP 
- GET
- /api/v1/erps/__uuid__/stop

#### 6. Start Running ERP 
- GET
- /api/v1/erps/__uuid__/start

