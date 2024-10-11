import inspect

class Emitter:
    def __init__(self) -> None:
        self._callbacks = {}

    # 获取事件的监听
    def listeners(self, event):
        eventName = '$' + event
        if eventName in self._callbacks:
            callbacks = self._callbacks[eventName]
            return callbacks
        else :
            return None

    # 添加事件监听
    def addEventListener(self, event, fn):
        fn.cbArgsLen = len(inspect.getargspec(fn).args)
        eventName = '$' + str(event)
        callbacks = None
        if (not eventName in self._callbacks):
            callbacks = []
            self._callbacks[eventName] = callbacks
        else:
            callbacks = self._callbacks[eventName]

        callbacks.append(fn)
        return self

    def on(self, event, fn):
        return self.addEventListener(event, fn)

    # 删除事件监听
    def removeEventListener(self, event, fn):
        if(event and fn):
            eventName = '$' + event
            if(not eventName in self._callbacks):#不存在
                return self
            callbacks = self._callbacks[eventName]
            callbacks.remove(fn)
            if(len(callbacks) <= 0):
                self._callbacks.pop(eventName)
        else:
            if(event):
                self._callbacks.pop(eventName)
            else:
                self._callbacks.clear()
        return self
    
    # 删除该事件的所以监听
    def removeAllListeners(self, event):
        eventName = '$' + event
        if(event):
            self._callbacks.pop(eventName)

    #派发事件
    def emit(self, event, *params):
        eventName = '$' + str(event)
        if (eventName in self._callbacks):
            callbacks = self._callbacks[eventName]
            for cb in callbacks:
                #cbArgsLen = len(inspect.getargspec(cb).args)
                cbArgsLen = cb.cbArgsLen
                paramLen = len(params)
                newParams = None
                if(paramLen == cbArgsLen):
                    newParams = params
                else:
                    newParams = []
                    for i in range(cbArgsLen):#cb需要的参数表
                        if(i<paramLen):
                            newParams.append(params[i])
                        else:
                            newParams.append(None)
                    newParams = tuple(newParams)
                cb(*newParams)
        return self
