// Your sbt build file. Guides on how to write one can be found at
// http://www.scala-sbt.org/0.13/docs/index.html
name := "TPCDS-Benchmark"

version := "0.1"

scalaVersion := "2.12.10"

crossScalaVersions := Seq("2.12.10")

// All Spark Packages need a license
licenses := Seq("Apache-2.0" -> url("http://opensource.org/licenses/Apache-2.0"))

sparkVersion := "3.0.0"

sparkComponents ++= Seq("sql", "hive", "mllib")

libraryDependencies += "com.github.scopt" %% "scopt" % "3.7.1"

libraryDependencies += "com.twitter" %% "util-jvm" % "6.45.0" % "provided"

libraryDependencies += "org.scalatest" %% "scalatest" % "3.0.5" % "test"

libraryDependencies += "org.yaml" % "snakeyaml" % "1.23"

fork := true

