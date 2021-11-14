from Goodmorning import ProductiveMorning

today = ProductiveMorning('Sacramento')

### test to do list
# checks case with no items on list
today.getToDoList()
# creates 4 objects on the to do list
today.addToDoList('wash car')
today.addToDoList('hair cut')
today.addToDoList('get groceries')
today.addToDoList('hug')
# displays to do list
today.getToDoList()
# removes completed item
today.removeToDoList('wash car')
# confirm item was removed
today.getToDoList()