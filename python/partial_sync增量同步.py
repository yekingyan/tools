from functools import wraps


class PartialSync(object):
    def __init__(self):
        self.m_listItem = []
        self.m_bCollect = False

    def CollectChangeItem(self, item):
        def Decorate(func):
            @wraps(func)
            def Wrapper(*args, **kwargs):
                res = func(*args, **kwargs)
                self._OnItemChange(item)
                return res

            Wrapper.func_closure_for_reload = func
            return Wrapper

        return Decorate

    def _OnItemChange(self, item):
        if not self.m_bCollect:
            return
        if item in self.m_listItem:
            return
        self.m_listItem.append(item)

    def RegisterSyncChange(self, *args, **kwargs):
        def _BeforeSyncChange():
            self.m_bCollect = True
            self.m_listItem = []
            self.BeforeSyncChange(*args, **kwargs)

        def _AfterSyncChange():
            self.m_bCollect = False
            self.AfterSyncChange(*args, **kwargs)

        def Decorate(func):
            @wraps(func)
            def Wrapper(*ar, **kw):
                _BeforeSyncChange()
                res = func(*ar, **kw)
                self.SyncChange(*args, **kwargs)
                _AfterSyncChange()
                return res

            Wrapper.func_closure_for_reload = func
            return Wrapper

        return Decorate

    def BeforeSyncChange(self, *args, **kwargs):
        pass

    def SyncChange(self, *args, **kwargs):
        raise NotImplementedError

    def AfterSyncChange(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    class Ps(PartialSync):
        def __init__(self):
            self.m_szPlayerID = None
            super(Ps, self).__init__()

        def SetPlayerID(self, szPlayerID):
            self.m_szPlayerID = szPlayerID

        def BeforeSyncChange(self, bSync2Gac=True, bSync2Gas=True):
            self.SetPlayerID(None)

        def SyncChange(self, bSync2Gac=True, bSync2Gas=True):
            print ("listItem", self.m_listItem)
            print ("bSync2Gac, bSync2Gas: {}".format((bSync2Gac, bSync2Gas)))
            print ("PlayerID", self.m_szPlayerID)

    ps = Ps()

    @ps.CollectChangeItem("a")
    def a(i, ii=1):
        print ("a", i, ii)

    @ps.CollectChangeItem("b")
    def b(j):
        print ("b", j)

    @ps.RegisterSyncChange(bSync2Gac=False)
    def m1():
        a(1, ii=11)
        b(2)
        a(1)
        ps.SetPlayerID("asdfasdf")

    m1()
    print "-"*50

    @ps.CollectChangeItem("c")
    def c(*x, **y):
        print ("c", x, y)

    @ps.RegisterSyncChange(bSync2Gas=False)
    def m2():
        c(3, a=33, b=333)

    m2()
