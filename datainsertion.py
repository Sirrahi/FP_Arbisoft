import json

from triumph import db
from triumph.models import Category, Product, SubCategory, Sku, ImageUrl


def get_or_create(model, **field):
    instance = db.session.query(model).filter_by(**field).first()
    if instance:
        return instance
    else:
        instance = model(**field)
        db.session.add(instance)
        return instance


db.create_all()

with open('data.json') as data_file:
    data = json.load(data_file)

for raw_product in data:
    category = get_or_create(Category, name=raw_product['category'][-2])

    sub_category = get_or_create(SubCategory, name=raw_product['sub_category'])
    category.sub_categories.append(sub_category)

    product = get_or_create(Product, id=int(raw_product['retailer_sku']), name=raw_product['name'],
                            brand=raw_product['brand'], price=raw_product['price'],
                            currency=raw_product['currency'], gender=raw_product['gender'],
                            description=raw_product['description'], url=raw_product['url'])
    category.products.append(product)
    sub_category.products.append(product)

    for image_url in raw_product['image_urls']:
        url = get_or_create(ImageUrl, url=image_url)
        product.image_urls.append(url)

    skus = raw_product['skus']

    if len(skus):
        for item in skus:
            sku = get_or_create(Sku, color=item['color'], size=item['size'],
                                price=item['price'], currency=item['currency'])
            for image_url in item['image_urls']:
                url = get_or_create(ImageUrl, url=image_url)
                sku.image_urls.append(url)

            product.skus.append(sku)

    db.session.commit()
