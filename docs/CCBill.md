# Test card

JCB: 3555555555555552

# CCBill webhook

## Example of query params

```
{
  "clientAccnum": "955063",
  "clientSubacc": "0000",
  "eventType": "NewSaleFailure",
  "eventGroupType": "Subscription"
}
```

## Example of webhook body

``` 
{
  "clientAccnum": "3333",
  "clientSubacc": "0000",
  "subscriptionId": "0125337302000000005",
  "transactionId": "0125337302000000005",
  "timestamp": "2025-12-03 10:17:56",
  "firstName": "ASD",
  "lastName": "FF",
  "address1": "Nema",
  "city": "Grad",
  "state": "Sisak-Moslavina county",
  "country": "HR",
  "postalCode": "10000",
  "email": "test@test.com",
  "ipAddress": "88.207.50.78",
  "formName": "0000",
  "priceDescription": "$0.99(USD) for 30 days (non-recurring)",
  "billedInitialPrice": "0.99",
  "billedRecurringPrice": "0.00",
  "billedCurrencyCode": "840",
  "billedCurrency": "USD",
  "subscriptionInitialPrice": "0.99",
  "subscriptionRecurringPrice": "0.00",
  "subscriptionCurrencyCode": "840",
  "subscriptionCurrency": "USD",
  "accountingInitialPrice": "0.99",
  "accountingCurrencyCode": "840",
  "accountingCurrency": "USD",
  "initialPeriod": "30",
  "recurringPeriod": "0",
  "rebills": "0",
  "dynamicPricingValidationDigest": "e87c...799c15af3",
  "paymentType": "CREDIT",
  "cardType": "JCB",
  "referringUrl": "none",
  "paymentAccount": "63347b...ee6e6dfcc11e2",
  "flexId": "b3a20b....c4ab4f93c",
  "threeDSecure": "NOT_APPLICABLE",
  "X-currencyCode": "840",
  "X-formDigest": "66aac6575f....f179",
  "X-paymentid": "fd5...02b2fc5403"
}```