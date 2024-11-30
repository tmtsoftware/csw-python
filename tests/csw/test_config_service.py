from csw.ConfigService import *


class TestConfigService:
    clientSession = ClientSession()
    configService = ConfigService(clientSession)

    async def test_config_service(self):
        if await self.configService.exists("foo"):
            await self.configService.delete("foo")
        configId = await self.configService.create("foo", ConfigData(bytes('hello', 'utf-8')), comment="test")
        x = await self.configService.getLatest('foo')
        assert (x.content.decode('utf-8') == 'hello')

        x2 = await self.configService.getById('foo', configId)
        assert (x2.content.decode('utf-8') == 'hello')

        x3 = await self.configService.getByTime('foo', datetime.now())
        assert (x3.content.decode('utf-8') == 'hello')

        x4 = await self.configService.getActive('foo')
        assert (x4.content.decode('utf-8') == 'hello')

        x5 = await self.configService.getActiveByTime('foo', datetime.now())
        assert (x5.content.decode('utf-8') == 'hello')
        assert await self.configService.getActiveVersion('foo') == configId

        infoList = [x for x in await self.configService.list() if x.path == "foo"]
        assert (infoList[0].path == "foo")
        assert (infoList[0].id == configId.id)
        assert (infoList[0].comment == "test")

        metadata = await self.configService.getMetadata()
        print(f'metadata = {metadata}')

        hist = await self.configService.history('foo',
                                                fromTime=datetime(2000, 1, 1),
                                                toTime=datetime.now(), maxResults=100)
        assert len(hist) == 1
        assert hist[0].id == configId.id

        hist2 = await self.configService.historyActive('foo')
        assert hist[0].id == hist2[0].id

        configId2 = await self.configService.update("foo", ConfigData(bytes('hello again', 'utf-8')), comment="test2")
        hist3 = await self.configService.history('foo')
        assert len(hist3) == 2
        assert hist3[1].id == configId.id
        assert hist3[0].id == configId2.id

        await self.configService.setActiveVersion('foo', configId, 'test3')
        x6 = await self.configService.getActive('foo')
        assert (x6.content.decode('utf-8') == 'hello')

        await self.configService.resetActiveVersion('foo', 'test4')
        x7 = await self.configService.getActive('foo')
        assert (x7.content.decode('utf-8') == 'hello again')
