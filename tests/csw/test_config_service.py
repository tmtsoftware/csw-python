from csw.ConfigService import ConfigService, ConfigData, FileType


class TestConfigService:
    configService = ConfigService()

    def test_create(self):
        id = self.configService.create("foo", ConfigData(bytes('hello', 'utf-8')))
        print(f'XXX create id = {id}')

    def test_list(self):
        for i in self.configService.list():
            print(f'XXX list() found {i.path}')
        for i in self.configService.list(FileType.Normal, '[a-z].*'):
            print(f'XXX list(Normal, [a-z].*) found {i.path}')

    def test_exists(self):
        b1 = self.configService.exists('XXX')
        print(f'XXX exists?: {b1}')
        b2 = self.configService.exists('yyy')
        print(f'yyy exists?: {b2}')
        b3 = self.configService.exists('zzz')
        print(f'zzz exists?: {b3}')

    def test_get_latest(self):
        x = self.configService.getLatest('XXX')
        print(f"XXX content of XXX is {x.content.decode('utf-8')}")
