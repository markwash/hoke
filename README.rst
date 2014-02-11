Helper for OpenStack Project Drivers
====================================

This project helps triaging Launchpad blueprints for OpenStack
projects. The name is a reference to the indomitable Hoke from
"Driving Miss Daisy." The connection is that OpenStack teams that
maintain blueprints are typically called "drivers".

Use
===

::

  hoke fetch <project name>  # downloads and caches all valid blueprints for the given project
  hoke show new  # list new blueprints for the project
  hoke show inconsistent  # list all inconsistent blueprints, along with a recommendation
  hoke show infowait  # show blueprints that need more info in most-recently-updated-first order
  hoke clear  # remove the local cache
