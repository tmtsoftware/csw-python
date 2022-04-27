import sbt._

object Libs {
  val ScalaVersion = "2.13.8"

  val `scala-async`     = "org.scala-lang.modules" %% "scala-async"     % "1.0.1"  //BSD 3-clause "New" or "Revised" License
}

object AkkaHttp {
  val Version                = "10.2.7"
  val `akka-http-spray-json` = "com.typesafe.akka" %% "akka-http-spray-json" % Version
}

object CSW {
//  val Version = "4.0.1"
//  val Version = "0.1.0-SNAPSHOT"
val Version = "3e85d6c312c79d0f28cd242793ff15774c91caf2"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
