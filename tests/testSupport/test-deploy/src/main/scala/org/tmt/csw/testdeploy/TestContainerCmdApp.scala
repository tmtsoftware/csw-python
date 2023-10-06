package org.tmt.csw.testdeploy

import csw.framework.deploy.containercmd.ContainerCmd
import csw.prefix.models.Subsystem

object TestContainerCmdApp {
  def main(args: Array[String]): Unit =
    ContainerCmd.start("testContainerCmdApp", Subsystem.withNameInsensitive("CSW"), args)
}
