lazy val aggregatedProjects: Seq[ProjectReference] = Seq(
  `test-assembly`,
  `test-hcd`,
  `test-deploy`
)

lazy val `pycsw-backend-test` = project
  .in(file("."))
  .aggregate(aggregatedProjects: _*)

lazy val `test-assembly` = project
  .settings(
    libraryDependencies ++= Dependencies.TestAssembly
  )

lazy val `test-hcd` = project
  .settings(
    libraryDependencies ++= Dependencies.TestHcd
  )

lazy val `test-deploy` = project
  .dependsOn(
    `test-assembly`,
    `test-hcd`
  )
  .enablePlugins(JavaAppPackaging, CswBuildInfo)
  .settings(
    libraryDependencies ++= Dependencies.TestDeploy
  )
