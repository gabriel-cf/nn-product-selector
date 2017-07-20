from .product_selector.modules.dataset_processing.src.io.mongoconnector.mongohandler import MongoHandler

if __name__ == '__main__':
    handler = MongoHandler.getInstance()
    i = 0
    for dbProduct in handler.getAllProducts():
        _id = dbProduct['_id']
        categories = dbProduct['sections']
        mainCategory = 'None'
        if categories and len(categories) > 0:
            mainCategory = categories[0]
        handler._productDB.products_collection.update_one({
          '_id': _id
        },{
          '$set': {
            'mainCategory': mainCategory
          }
        }, upsert=False)
        i += 1
        if i % 1000 == 0:
            print(i)
