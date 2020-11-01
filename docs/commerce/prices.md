## Prices
URL : /api/v1/prices/ 

- Price points must be unique for every number of erp and price.
- This is a price point of  'n' erp of 1 day.

#### 1. Get 
a. For single : 
- url : /api/v1/prices/__uuid__

b. For Multiple
- url : /api/v1/prices?__query__
- Accepeted values : start, lmt, price_gte, price_lte, erp_gte, erp_lte
[gte = greater than equal to, lte = less than equal to]
- example = /api/v1/prices?start=10&lmt=100

#### 2.POST
- Creates new Price point
- Only accessable by mods
- data format :
```
{
    'erp_number' : __int__,
    'price' : __float__
}
```

#### 3. Patch
- Updates created price point.
- url : /api/v1/prices/__uuid__
- format : 
```
{
    'erp_number' : __int__ / null,
    'price' : __float__ / null
}
```

#### 4. Delete
- Permanently deletes price
- url : /api/v1/prices/__uuid__
