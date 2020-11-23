## Purchase Invoices
URL : /api/v1/purchase/__uuid__

#### 1. Get 
a. For Multiple
- url : /api/v1/purchase
- Accepeted values : start, lmt, bill_amount_gte, bill_amount_lte, hours_lte, hours_gte, erp_gte, erp_lte
- example = /api/v1/purchase?start=10&lmt=100

b. For Single
- url : /api/v1/purchase/credits/__credits_uuid__

#### 2. POST
- For adding new purchase after payment verification
```
{
    hours : __int__,
    number_of_erps : __int__,
    pure_total_amount : __float__,
    paid_amount : __float__,
    bill_amount : __float__,
    discount_amount : __float__,
    discount_note : __str__,
    payment_verifcation : __json__,
    extended_credit : [
        __credit_id__, . . . 
    ] / None
}
```

#### 3.Patch
- Used to trigger refund
```
{
    'do' : 'refund'
}
```
