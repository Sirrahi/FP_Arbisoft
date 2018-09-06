from triumph import db
from triumph.models import Category, Product, Feature, Sku, ImageUrl
import json


def get_or_create(model, **field):
    instance = db.session.query(model).filter_by(**field).first()
    if instance:
        return instance
    else:
        instance = model(**field)
        return instance


db.create_all()

with open('data.json') as data_file:
    data = json.load(data_file)

for raw_product in data:

    category = get_or_create(Category, name=raw_product['category'][-2])
    db.session.add(category)

    feature = get_or_create(Feature, name=raw_product['feature'])
    db.session.add(feature)
    category.features.append(feature)

    product = Product(id=int(raw_product['retailer_sku']), name=raw_product['name'], brand=raw_product['brand'],
                      gender=raw_product['gender'], description=raw_product['description'], url=raw_product['url'])
    db.session.add(product)
    feature.products.append(product)
    product.category.append(category)

    for image_url in raw_product['image_urls']:
        url = ImageUrl(url=image_url)
        db.session.add(url)
        product.image_urls.append(url)

    skus = raw_product['skus']

    for i in range(1, len(skus)):
        sku = Sku(color=skus['%d' % i]['color'], size=skus['%d' % i]['size'],
                  price=skus['%d' % i]['price'], currency=skus['%d' % i]['currency'])

        db.session.add(sku)

        for image_url in skus['%d' % i]['image_urls']:
            url = ImageUrl(url=image_url)
            db.session.add(url)
            sku.image_urls.append(url)

        product.skus.append(sku)

    db.session.commit()
