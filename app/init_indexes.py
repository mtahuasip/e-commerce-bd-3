def create_indexes(db):
    db.users.create_index("email", unique=True)
    # db.products.create_index("title")
