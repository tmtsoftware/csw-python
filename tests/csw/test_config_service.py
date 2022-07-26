from datetime import datetime, timezone

from csw.ConfigService import ConfigService, ConfigData, FileType


class TestConfigService:
    configService = ConfigService()

    def test_config_service(self):
        if self.configService.exists("foo"):
            self.configService.delete("foo")
        id = self.configService.create("foo", ConfigData(bytes('hello', 'utf-8')), comment="test")
        x = self.configService.getLatest('foo')
        assert (x.content.decode('utf-8') == 'hello')
        x2 = self.configService.getById('foo', id)
        assert (x2.content.decode('utf-8') == 'hello')
        x3 = self.configService.getByTime('foo', datetime.now(timezone.utc))
        assert (x3.content.decode('utf-8') == 'hello')
        x4 = self.configService.getActive('foo')
        assert (x4.content.decode('utf-8') == 'hello')
        x5 = self.configService.getActiveByTime('foo', datetime.now(timezone.utc))
        assert (x5.content.decode('utf-8') == 'hello')
        assert self.configService.getActiveVersion('foo') == id
        list = [x for x in self.configService.list() if x.path == "foo"]
        assert (list[0].path == "foo")
        assert (list[0].id == id.id)
        assert (list[0].comment == "test")
        metadata = self.configService.getMetadata()
        print(f'metadata = {metadata}')
        hist = self.configService.history('foo',
                                          fromTime=datetime(2000, 1, 1, tzinfo=timezone.utc),
                                          toTime=datetime.now(tz=timezone.utc), maxResults=100)
        assert len(hist) >= 1
        assert hist[0].id == id.id
        hist2 = self.configService.historyActive('foo')
        assert hist[0].id == hist2[0].id
        # TODO: test server for why results of historyActive() and history() have different times and lengths!

