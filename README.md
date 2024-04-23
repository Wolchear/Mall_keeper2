# Mall keeper

## How to launch
```git clone```

```docker-compose up```



## Endpoints
```
/shops
/shops/goods
/workers
```

## Sample Data
### Good
```
{
	'name': "Milk",
	'good_type': "diary product"
}
```
### Worker
```
{
	'name': "Davina",
	'surname': "Keith",
	'shop': "Maxima",
	'Mall_id': 1,
	'Id_in_shop': 1
}
```

### Shop
```
{
	'shop_id': 1,
	'name': "flowers_shop",
	'floor': 1,
	'goods': good_list,
	'workers': workers_list
}
```


### Get
All shops:
```curl -X GET http://127.0.0.1:5000/shops```

All mall workers:
```curl http://127.0.0.1:5000/workers```

Worker by Mall id:
```curl -X GET "http://127.0.0.1:5000/workers?mall_id=1"```

All goods in shop by shop id:
```curl -X GET "http://127.0.0.1:5000/shops/goods?shop_id=123"```

### Post
Add New shop:
```curl -X POST -H "Content-Type: application/json" -d '{"name":"New Shop", "floor": 1}' http://127.0.0.1:5000/shops```

Add new good:
```curl -X POST -H "Content-Type: application/json" -d '{"good_name":"Apple", "good_type":"Fruit", "shop_id": 1}' http://127.0.0.1:5000/shops/goods```

Add new worker to the shop:
```curl -X POST -H "Content-Type: application/json" -d '{"worker_name":"Name", "worker_surname":"Surname", "shop_id": 1}' http://127.0.0.1:5000/workers```

### Put
Update shop name and\or floor:
```curl -X PUT -H "Content-Type: application/json" -d '{"shop_id": 1, "new_name": "new_name", "new_floor": 2}' http://127.0.0.1:5000/shops```

### Delete
Delete shop by id:
```curl -X DELETE -H "Content-Type: application/json" -d '{"shop_id": 123}' http://127.0.0.1:5000/shops```

Delete good by name in shop:
```curl -X DELETE -H "Content-Type: application/json" -d '{"shop_id": 1, "good_name": "Milk"}' http://127.0.0.1:5000/shops/goods```


