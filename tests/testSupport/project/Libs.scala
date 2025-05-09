import sbt._

object Libs {
  val ScalaVersion = "3.6.4"
}

object CSW {
  val Version = "6.0.0"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
