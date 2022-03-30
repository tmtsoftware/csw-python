addSbtPlugin("org.scalastyle" %% "scalastyle-sbt-plugin" % "1.0.0")

addSbtPlugin("org.scalameta" % "sbt-scalafmt" % "2.4.6")
addSbtPlugin("com.typesafe.sbt" % "sbt-native-packager" % "1.5.1")
addSbtPlugin("com.eed3si9n" % "sbt-buildinfo" % "0.9.0")

classpathTypes += "maven-plugin"

scalacOptions ++= Seq(
  "-encoding",
  "UTF-8",
  "-feature",
  "-unchecked",
  "-deprecation",
  // "-Xfatal-warnings",
  "-Xlint:-unused,_",
  "-Ywarn-dead-code"
)
resolvers += "jitpack" at "https://jitpack.io"
