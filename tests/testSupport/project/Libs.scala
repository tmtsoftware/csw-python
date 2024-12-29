import sbt._

object Libs {
  val ScalaVersion = "3.6.2"
}

object CSW {
//  val Version = "5.0.0"
val Version = "919e345"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
