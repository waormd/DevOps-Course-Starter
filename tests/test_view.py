from todo.view import ViewModel
from todo.item import Item

def example_items():
    return example_todo_items() + example_in_progress_items() + example_done_items() 

def example_todo_items():
    return [
        Item(0, 'Todo', 'A Title', 'aDateTime'),
        Item(1, 'Todo', 'A Title', 'aDateTime')
    ]

def example_in_progress_items():
    return [
        Item(2, 'In progress', 'A Title', 'aDateTime'),
        Item(3, 'In progress', 'A Title', 'aDateTime')
    ]

def example_done_items():
    return [
        Item(4, 'Done', 'A Title', 'aDateTime'),
        Item(5, 'Done', 'A Title', 'aDateTime')
    ]

def test_todo_items():
    view = ViewModel(example_items())
    assert view.todo_items == example_todo_items()

def test_in_progress_items():
    view = ViewModel(example_items())
    assert view.in_progress_items == example_in_progress_items()

def test_done_items():
    view = ViewModel(example_items())
    assert view.done_items == example_done_items()



