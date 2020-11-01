## Bundles
URL : /api/v1/bundles/ 

#### 1. Get 
a. For single : 
- url : /api/v1/bundles/__uuid__

b. For Multiple
- url : /api/v1/bundles?__query__
- Accepeted values : start, lmt, price_gte, price_lte, days_lte, days_gte, erp_gte, erp_lte
[gte = greater than equal to, lte = less than equal to]
- example = /api/v1/bundles?start=10&lmt=100

#### 2.POST
- Creates new bundle
- Only accessable by mods
- data format :
```
{
    'time_in_days' : __int__,
    'number_of_erp' : __int__,
    'price' : __float__
}
```

#### 3. Patch
- Updates created bundle
- url : /api/v1/bundles/__uuid__
- format : 
```
{
    'time_in_days' : __int__ / null ,
    'number_of_erp' : __int__ / null,
    'price' : __float__ / null
}
```

#### 4. Delete
- Permanently deletes bundle
- url : /api/v1/bundles/__uuid__
