import sbt._

object Libs {
  val ScalaVersion = "3.3.3"
}

object CSW {
//  val Version = "5.0.0"
val Version = "1ecfbb3"

  val `csw-framework` = "com.github.tmtsoftware.csw" %% "csw-framework" % Version
  val `csw-testkit`   = "com.github.tmtsoftware.csw" %% "csw-testkit" % Version
}
