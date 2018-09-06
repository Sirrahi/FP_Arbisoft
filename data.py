from triumph import db
from triumph.models import Category, Item, Feature, Sku, ImageUrl
import json


# def get_or_create(model, **field):
#     instance = db.session.query(model).filter_by(**field).first()
#     if instance:
#         return instance
#     else:
#         instance = model(**field)
#         return instance
#
#
# db.create_all()
#
# with open('data.json') as data_file:
#     data = json.load(data_file)
#
# for raw_product in data:
#
#     category = get_or_create(Category, name=raw_product['category'][-2])
#
#     db.session.add(category)
#
#     item = Item(id=int(raw_product['retailer_sku']), name=raw_product['name'], brand=raw_product['brand'],
#                 description=raw_product['description'], url=raw_product['url'])
#
#     db.session.add(item)
#
#     item.category.append(category)
#
#     for image_url in raw_product['image_urls']:
#         url = ImageUrl(url=image_url)
#         db.session.add(url)
#         item.image_urls.append(url)
#
#     feature = get_or_create(Feature, name=raw_product['category'][0])
#
#     db.session.add(feature)
#
#     item.features.append(feature)
#
#     skus = raw_product['skus']
#
#     for i in range(1, len(skus)):
#         sku = Sku(color=skus['%d' % i]['color'], size=skus['%d' % i]['size'],
#                   price=skus['%d' % i]['price'], currency=skus['%d' % i]['currency'])
#
#         db.session.add(sku)
#
#         for image_url in skus['%d' % i]['image_urls']:
#             url = ImageUrl(url=image_url)
#             db.session.add(url)
#             sku.image_urls.append(url)
#
#         item.skus.append(sku)
#
#     db.session.commit()


# categories = Category.query.all()
# for category in categories:
#     print('Category: ', category.name)
#     for item in category.items:
#         print('UID: ', item.id)
#         print('Item: ', item.name)
#         print('Brand: ', item.brand)
#         print('Description: ', item.description)
#         for url in item.image_urls:
#             print('url: ', url.url)
#         for feature in item.features:
#             print('Feature: ', feature.name)
#         for sku in item.skus:
#             print()
#             print('sku_id: ', sku.id)
#             print('color: ', sku.color)
#             print('size: ', sku.size)
#             print('prize: ', sku.price)
#             for url in sku.image_urls:
#                 print('url: ', url.url)

# categories = Category.query.all()
# print('CATEGORIES')
# for category in categories:
#     print(category.name)
# print()
#
# features = Feature.query.all()
# print('FEATURES')
# for feature in features:
#     print(feature.name)
# print()

# urls = ImageUrl.query.all()
# print('URLS')
# for url in urls:
#     print(url.url)

skus = Sku.query.filter_by(color='Shocking Blue').all()
image_urls = []
for sku in skus:
    for image_url in sku.image_urls:
        image_urls.append(image_url.url)

    print({'id': sku.id, 'color': sku.color, 'size': sku.size, 'price': sku.price,
           'currency': sku.currency, 'image_urls': image_urls})

product = Item.query.get(10185067)
print(product.image_urls[0].url)