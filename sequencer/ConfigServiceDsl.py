from aiohttp import ClientSession

from csw.ConfigService import ConfigService


class ConfigServiceDsl:
    def __init__(self, clientSession: ClientSession):
        self.configService = ConfigService(clientSession)

    async def existsConfig(self, path: str, id: str = None) -> bool:
        """
        Checks if configuration file exists at provided path

        Args:
            path: relative configuration file path
            id: optional revision of the file

        Returns:
            true if the file exists, false otherwise
        """
        return await self.configService.exists(path, id)

    # XXX TODO FIXME: Needs HOCON support in python?
    # def getConfig(self, path: str) -> bool:
    #     """
    #     Retrieves active configuration file contents present at provided path
    #
    #     Args:
    #         path: relative configuration file path
    #
    #     Returns:
    #         file content as [Config] object if file exists, otherwise returns null
    #     """
    #     configData = self.configService.getActive(path)
    #     if configData:
    #         return configData.toJConfigObject(actorSystem)?.await()

