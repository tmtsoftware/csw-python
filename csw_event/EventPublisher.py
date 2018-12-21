from csw_event.RedisConnector import RedisConnector


class EventPublisher:

    def __init__(self):
        self.__redis = RedisConnector()

    def publish(self, pb_event):
        '''
        Publish a PbEvent to Event Service

        :param pb_event: Event to be published, as a PbEvent type
        :return: None
        '''
        event_key = pb_event.source + "." + pb_event.name
        self.__redis.publish(event_key, pb_event.SerializeToString())
