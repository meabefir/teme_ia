class EventManager:
    SUBSCRIPTIONS = {}

    @staticmethod
    def connect(signal_name, callback):
        if signal_name in EventManager.SUBSCRIPTIONS:
            EventManager.SUBSCRIPTIONS[signal_name] += [callback]
        else:
            EventManager.SUBSCRIPTIONS[signal_name] = [callback]

    @staticmethod
    def disconnect(signal_name, callback):
        if signal_name not in EventManager.SUBSCRIPTIONS:
            return
        EventManager.SUBSCRIPTIONS[signal_name].remove(callback)

    @staticmethod
    def emit_signal(signal, *args):
        for callback in EventManager.SUBSCRIPTIONS[signal]:
            callback(args)