import sbt._

object Libs {
  val ScalaVersion = "3.3.1"
}

//object PekkoHttp {
//  val Version = "1.0.0"
//  val Org     = "org.apache.pekko"
//
//  val `pekko-http-spray-json` = Org %% "pekko-http-spray-json" % Version
//}

object CSW {
//  val Version = "5.0.0"
val Version = "6f29ed1"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
