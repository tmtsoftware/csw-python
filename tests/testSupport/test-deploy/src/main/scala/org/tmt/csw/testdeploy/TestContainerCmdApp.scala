package org.tmt.csw.testdeploy

import csw.framework.deploy.containercmd.ContainerCmd
import csw.prefix.models.Subsystem

object TestContainerCmdApp extends App {

  ContainerCmd.start("testContainerCmdApp", Subsystem.withNameInsensitive("CSW"), args)

}
