def loading(func):
    def func_wrapper(smthing, parent, **kwargs):
        parent.pb.visible = True
        parent.page.update()

        val = func(smthing, parent, **kwargs)

        parent.pb.visible = False
        parent.page.update()

        return val

    return func_wrapper
