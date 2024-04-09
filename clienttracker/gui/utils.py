def del_obj(obj, parent):
    obj.remove()
    parent.update_tab(None)


def edit_obj(obj, parent):
    parent.notify('В разработке')
    pass
