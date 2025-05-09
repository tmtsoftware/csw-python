import pytest

from csw.ConfigService import *


@pytest.mark.asyncio
class TestConfigService:

    async def test_config_service(self):
        clientSession = ClientSession()
        configService = ConfigService(clientSession)
        if await configService.exists("foo"):
            await configService.delete("foo")
        configId = await configService.create("foo", ConfigData(bytes('hello', 'utf-8')), comment="test")
        x = await configService.getLatest('foo')
        assert (x.content.decode('utf-8') == 'hello')

        x2 = await configService.getById('foo', configId)
        assert (x2.content.decode('utf-8') == 'hello')

        x3 = await configService.getByTime('foo', datetime.now())
        assert (x3.content.decode('utf-8') == 'hello')

        x4 = await configService.getActive('foo')
        assert (x4.content.decode('utf-8') == 'hello')

        x5 = await configService.getActiveByTime('foo', datetime.now())
        assert (x5.content.decode('utf-8') == 'hello')
        assert await configService.getActiveVersion('foo') == configId

        infoList = [x for x in await configService.list() if x.path == "foo"]
        assert (infoList[0].path == "foo")
        assert (infoList[0].id == configId.id)
        assert (infoList[0].comment == "test")

        metadata = await configService.getMetadata()
        print(f'metadata = {metadata}')

        hist = await configService.history('foo',
                                                fromTime=datetime(2000, 1, 1),
                                                toTime=datetime.now(), maxResults=100)
        assert len(hist) == 1
        assert hist[0].id == configId.id

        hist2 = await configService.historyActive('foo')
        assert hist[0].id == hist2[0].id

        configId2 = await configService.update("foo", ConfigData(bytes('hello again', 'utf-8')), comment="test2")
        hist3 = await configService.history('foo')
        assert len(hist3) == 2
        assert hist3[1].id == configId.id
        assert hist3[0].id == configId2.id

        await configService.setActiveVersion('foo', configId, 'test3')
        x6 = await configService.getActive('foo')
        assert (x6.content.decode('utf-8') == 'hello')

        await configService.resetActiveVersion('foo', 'test4')
        x7 = await configService.getActive('foo')
        assert (x7.content.decode('utf-8') == 'hello again')
