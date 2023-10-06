package org.tmt.csw.testdeploy

import csw.framework.deploy.hostconfig.HostConfig
import csw.prefix.models.Subsystem

object TestHostConfigApp {
  def main(args: Array[String]): Unit =
    HostConfig.start("test-host-config-app", Subsystem.withNameInsensitive("CSW"), args)
}
