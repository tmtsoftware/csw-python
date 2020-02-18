import org.scalafmt.sbt.ScalafmtPlugin.autoImport.scalafmtOnCompile
import sbt.Keys._
import sbt.{Resolver, url, _}
import sbt.plugins.JvmPlugin

object Common extends AutoPlugin {

  override def trigger: PluginTrigger = allRequirements

  override def requires: Plugins = JvmPlugin

  override lazy val projectSettings: Seq[Setting[_]] = Seq(
    organization := "org.tmt",
    organizationName := "TMT",
    scalaVersion := Libs.ScalaVersion,
    organizationHomepage := Some(url("http://www.tmt.org")),

    dependencyOverrides += AkkaHttp.`akka-http-spray-json`,

    scalacOptions ++= Seq(
      "-encoding",
      "UTF-8",
      "-feature",
      "-unchecked",
      "-deprecation",
      "-Xlint",
      "-Ywarn-dead-code",
    ),
    javacOptions in (Compile, doc) ++= Seq("-Xdoclint:none"),
    testOptions in Test ++= Seq(
      // show full stack traces and test case durations
      Tests.Argument("-oDF"),
      // -v Log "test run started" / "test started" / "test run finished" events on log level "info" instead of "debug".
      // -a Show stack traces and exception class name for AssertionErrors.
      Tests.Argument(TestFrameworks.JUnit, "-v", "-a")
    ),
    resolvers += "jitpack" at "https://jitpack.io",
    resolvers += "bintray" at "https://jcenter.bintray.com",
    version := "0.0.1",
    fork := true,
    parallelExecution in Test := false,
    autoCompilerPlugins := true,
    if (formatOnCompile) scalafmtOnCompile := true else scalafmtOnCompile := false
  )

  private def formatOnCompile = sys.props.get("format.on.compile") match {
    case Some("false") ⇒ false
    case _             ⇒ true
  }
}
