## Purchases Settings
URL : /api/v1/purchase/settings/__uuid__


#### 1. Get 
- url : /api/v1/purchase/settings/


#### 2. Patch
- Updates created price point.
- url : /api/v1/purchase/settings/__uuid__
- format : 
```
{
    'unitary_price' : __int__ / null
}
```