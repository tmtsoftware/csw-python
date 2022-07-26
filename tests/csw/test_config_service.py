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
        list = [x for x in self.configService.list() if x.path == "foo"]
        assert (list[0].path == "foo")
        assert (list[0].id == id.id)
        assert (list[0].comment == "test")