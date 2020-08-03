class Item:
    def __init__(self, itemId, status, title):
        self.id = itemId
        self.status = status
        self.title = title

    def __eq__(self, item):
        if self.id == item.id and self.status == item.status and self.title == item.title:
            return True
        return False

    def __repr__(self):
        return f'Item{{id={self.id},status={self.status},title={self.title}}}'
