from datetime import date, datetime 

class ViewModel:
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return [ x for x in self._items if x.status == 'Todo' ]

    @property
    def in_progress_items(self):
        return [ x for x in self._items if x.status == 'In progress' ]

    @property
    def done_items(self):
        return [ x for x in self._items if x.status == 'Done' ]

    @property
    def recent_done_items(self):
        return [ x for x in self._items if datetime.strptime(x.lastModified, "%Y-%m-%dT%H:%M:%S.%fZ") > datetime.combine(date.today(), datetime.min.time())]

    @property
    def old_done_items(self):
        return [ x for x in self._items if datetime.strptime(x.lastModified, "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.combine(date.today(), datetime.max.time())]