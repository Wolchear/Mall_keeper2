# Mall keeper

## How to launch
```git clone --recursive <url>```
```docker-compose up```

## Endpoints
```
/shops
/shops/<shop_id>
/shops/<shop_id>/goods
/shops/<shop_id>/goods/<good_id>
/shops/<shop_id>/workers/<worker_id>
/workers
/workers/<mall_id>
```

## Sample Data
### Good
```
{
	'name': "Milk",
	'good_type': "diary product",
	'good_id': 1
}
```
### Worker
```
{
	'name': "Davina",
	'surname': "Keith",
	'shop': "Maxima",
	'Mall_id': 1,
	'Id_in_shop': 1,
	'Sex': "Female",
	'Salary': 1000,
	'Position': "Manager"
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

```curl -X GET http://172.24.0.3:80/shops```

All mall workers:

```curl http://172.24.0.3:80/workers```

Worker by Mall id:

```curl -X GET http://172.23.0.3:80/workers/2```

All goods in shop by shop id:

```curl -X GET http://172.23.0.3:80/shops/1/goods```

### Post
Add New shop:

```curl -X POST -H "Content-Type: application/json" -d '{"name":"New Shop", "floor": 1}' http://172.24.0.3:80/shops```

Add new good:

```curl -X POST -H "Content-Type: application/json" -d '{"good_name":"Apple", "good_type":"Fruit"}'  http://172.24.0.3:80/shops/1/goods```

Add new worker to the shop:

```curl -X POST -H "Content-Type: application/json" -d '{"worker_name": "John", "worker_surname": "Doe", "sex": "male", "position": "Cashier", "salary": 700}' http://172.24.0.3:80/shops/1/workers```

### Put
Update shop name and\or floor:

```curl -X PUT -H "Content-Type: application/json" -d '{"new_name": "new_name", "new_floor": 2}' http://127.0.0.1:80/shops/1```

Update worker:

```curl -X PUT -H "Content-Type: application/json" -d '{"salary": 3500, "position": "Manager"}' http://172.24.0.3:80/shop/1/workers/1```

### Delete
Delete shop by id:

```curl -X DELETE http://172.23.0.3:80/shops/1```

Delete good in shop:

```curl -X DELETE  http://172.23.0.3:80/shops/2/goods/1```

Delete worker in shop:

```curl -X DELETE  http://172.23.0.3:80/shops/2/workers/1```


