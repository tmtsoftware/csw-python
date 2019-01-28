from csw_event.RedisConnector import RedisConnector


class EventPublisher:

    def __init__(self):
        self.__redis = RedisConnector()

    def publish(self, pb_event):
        '''
        Publish a PbEvent to the Event Service

        :param PbEvent pb_event: Event to be published
        :return: None
        '''
        event_key = pb_event.source + "." + pb_event.name
        self.__redis.publish(event_key, pb_event.SerializeToString())

    def publishSystemEvent(self, event):
        '''
        Publish a SystemEvent to the Event Service

        :param SystemEvent event: event to be published
        :return: None
        '''
        self.publish(event.pbEvent)
