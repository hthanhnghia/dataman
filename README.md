# Dataman
a version controlled key-value storage supporting HTTP GET/POST request.

# Platform and techniques used
Django web framework + Redis db

# Usage
- **GET /object/:key(?timestamp)** : get the value of the key

| Parameter name | Parameter description | Type
| ------ | ------ | ------ |
| key | (Required) The key that we want to get the value | String
| timestamp | (Optional) Unix timestamp. When provided, the value of the key at this timestamp will be returned | Number

**Example**:
```
Request: /object/key
Response: 'value'
```

- **POST /object** : post the key-value data to the db  

**Example**:
```
Request: /object
Body: {'mykey' : 'value'}
```
