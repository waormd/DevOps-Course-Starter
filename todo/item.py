class Item:
    def __init__(self, itemId, status, title, lastModified):
        self.id = itemId
        self.status = status
        self.title = title
        self.lastModified = lastModified

    def __eq__(self, item):
        if self.id == item.id and self.status == item.status and self.title == item.title and self.lastModified == item.lastModified:
            return True
        return False

    def __repr__(self):
        return f'Item{{id={self.id},status={self.status},title={self.title},lastModified={self.lastModified}}}'
