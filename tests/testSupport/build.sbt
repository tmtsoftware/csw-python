lazy val aggregatedProjects: Seq[ProjectReference] = Seq(
  `test-assembly`,
  `test-deploy`
)

lazy val `pycsw-backend-test` = project
  .in(file("."))
  .aggregate(aggregatedProjects: _*)

lazy val `test-assembly` = project
  .settings(
    libraryDependencies ++= Dependencies.TestAssembly
  )

lazy val `test-deploy` = project
  .dependsOn(
    `test-assembly`
  )
  .enablePlugins(JavaAppPackaging, CswBuildInfo)
  .settings(
    libraryDependencies ++= Dependencies.TestDeploy
  )
