from triumph import db
from triumph.models import Category, Product, SubCategory, Sku, ImageUrl
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
#     db.session.add(category)
#
#     sub_category = get_or_create(SubCategory, name=raw_product['sub_category'])
#     db.session.add(sub_category)
#     category.sub_categories.append(sub_category)
#
#     product = Product(id=int(raw_product['retailer_sku']), name=raw_product['name'], brand=raw_product['brand'],
#                       gender=raw_product['gender'], description=raw_product['description'], url=raw_product['url'])
#     db.session.add(product)
#     sub_category.products.append(product)
#     product.category.append(category)
#
#     for image_url in raw_product['image_urls']:
#         url = ImageUrl(url=image_url)
#         db.session.add(url)
#         product.image_urls.append(url)
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
#         product.skus.append(sku)
#
#     db.session.commit()

product = Product.query.get(10186060)
# print(product.url)

for sku in product.skus:
    for url in sku.image_urls:
        print(url.url)
    print()