def create_indexes(db):
    db.users.create_index("email", unique=True)
    db.categories.create_index("name", unique=True)
    db.products.create_index("name", unique=True)
