package org.tmt.csw.testhcd

import csw.location.api.models.Connection.AkkaConnection
import csw.location.api.models.{ComponentId, ComponentType}
import csw.prefix.models.Prefix
import csw.testkit.scaladsl.CSWService.{AlarmServer, EventServer}
import csw.testkit.scaladsl.ScalaTestFrameworkTestKit
import org.scalatest.FunSuiteLike

import scala.concurrent.Await
import scala.concurrent.duration._

class TestHcdTest extends ScalaTestFrameworkTestKit(AlarmServer, EventServer) with FunSuiteLike {

  import frameworkTestKit.frameworkWiring._

  override def beforeAll(): Unit = {
    super.beforeAll()
    // uncomment if you want one HCD run for all tests
    spawnStandalone(com.typesafe.config.ConfigFactory.load("TestHcdStandalone.conf"))
  }

  test("HCD should be locatable using Location Service") {
    val connection = AkkaConnection(ComponentId(Prefix("CSW.TestHcd"), ComponentType.HCD))
    val akkaLocation = Await.result(locationService.resolve(connection, 10.seconds), 10.seconds).get

    akkaLocation.connection shouldBe connection
  }
}