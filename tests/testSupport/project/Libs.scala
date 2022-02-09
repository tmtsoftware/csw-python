import sbt._

object Libs {
  val ScalaVersion = "2.13.1"

  val `scala-async`     = "org.scala-lang.modules" %% "scala-async"     % "0.10.0"  //BSD 3-clause "New" or "Revised" License
}

object AkkaHttp {
  val Version                = "10.2.0"
  val `akka-http-spray-json` = "com.typesafe.akka" %% "akka-http-spray-json" % Version
}

object CSW {
  val Version = "4.0.1"
//  val Version = "0.1.0-SNAPSHOT"
//val Version = "a9073713d8b5de90a817e08b31629a7176e1b4fe"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
