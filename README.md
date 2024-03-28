# AntikDecor

## Product
* Product List `GET` `=>` `products/?category_id={}&sidebar_id={}&search={}&page={}`
```json
{
    "count": 100,
    "next": "https://...",
    "previous": "https://...",
    "results": [
        {
            "id": 1000,
            "name": "...",
            "catalog": "...",
            "price": 30000,
            "images": [
                "https://..."
            ]
        },
        "... other results"
    ]
}
```
* Product Detail `GET` `=>` `product/<product_id>/`
```json
{
    "id": 2595,
    "name": "...",
    "price": 20000,
    "vendor_code": "...",
    "history": "...",
    "characteristic": "...",
    "size": "...",
    "images": [
        "https://..."
    ],
    "video_url": "https://...",
    "description": "..."
}
```
* New Products `GET` `=>` `new-products/`
```json
[
    {
        "id": 1000,
        "name": "...",
        "catalog": "...",
        "price": 15000,
        "images": [
            "https://..."
        ]
    },
    "... other results"
]
```
* Category Detail `GET` `=>` `category/<category_id>/`
```json
{
    "id": 1,
    "name": "...",
    "subcategories": [
        {
            "id": 10,
            "name": "..."
        },
        "... other results"
    ]
}
```
* Category Sidebar `GET` `=>` `category/<category_id>/sidebar/`
```json
{
    "data": [
        {
            "id": 1,
            "name": "...",
            "subcategories": [
                {
                    "id": 10,
                    "name": "..."
                },
                "... other results"
            ]
        },
        "... other results"
    ]
}
```

## Main Page
* News List `GET` `=>` `news/`
```json
[
    {
        "id": "efa06612-cc9e-455a-9430-2c258b448df4",
        "date": "2024-03-28",
        "image": "https://...",
        "title": "...",
        "content": "..."
    },
    "... other results"
]
```
* News Detail `GET` `=>` `news/<news_id>/`
```json
{
    "id": "efa06612-cc9e-455a-9430-2c258b448df4", 
    "date": "2024-03-28",
    "image": "https://...",
    "title": "...", 
    "content": "..."
}
```
* Banner List `GET` `=>` `banners/`
```json
[
    {
        "title": "...",
        "subtitle": "...",
        "image": "https://..."
    },
    "... other results"
]
```
* Videos List `GET` `=>` `videos/`
```json
[
    {
        "title": "...",
        "url": "https://www.youtube.com/...",
        "banner": "https://..."
    },
    "... other results"
]
```

## Order
* Order `POST` `=>` `order/`

request
```json
{
  "customer_name": "...",
  "customer_phone": "...",
  "customer_email": "...@...com",
  "customer_address": "...",
  "total_price": 100000,
  "products": [
    1001, 1002, "..."
  ]
}
```
response
```json
{
    "success": true,
    "message": "Order saved!"
}
```

*  `POST` `=>` `callback/`

request
```json
{
  "applicant_name": "...",
  "applicant_email": "...@gmail.com"
}
```
response
```json
{
    "success": true,
    "message": "Callback data saved!"
}
```

