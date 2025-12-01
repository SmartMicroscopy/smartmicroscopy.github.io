# Guidelines for contribution

## Introduction

Development of this material is a joint effort of the members of the Smart Microscopy Working Group (SMWG). Group members representing both academia and industry organisations are welcome to contribute to these modules in the following ways:
* Revising existing modules
* Developing new modules.
* Adding activities and implementations to the existing modules

Below you find guidelines for different kinds of contributions. If you have any questions, please contact *SMWG group admins*.

:::{note}
This is the first version of contribution notes developed from the perspective that only a few group members might contribute to this activity in the initial project phase. When more people will contribute to these activities, guidelines are to be revised to simplify the contribution process.
:::


## Revising existing modules

Individual modules are currently hosted by the [Bioimage Analysis Training Resources](https://neubias.github.io/training-resources/). Both core (platform independent) parts of the modules and individual activities can be revised at any moment in one of the following ways depending on your experience and number of edits to be introduced:

### Option 1: Offline editing (recommended for minor edits)

* Print the entire unit or part of it to a PDF file from your browser.
* Add comments with changes and suggestions to this file.
* Send the PDF file with comments to **SMWG group admins**.

### Option 2: Online editing

* Request **SMWG group admins** to become an editor of the [Bioimage Analysis Training Resources repository](https://neubias.github.io/training-resources/).
* Find (or request **SMWG group admins**) the links of .md files containing modules you would like to edit.
* Create a new branch and introduce your changes.
* Make a merge request for the changes to be propagated to the main branch (assign @ssgpers to be responsible for this merge request).

## Developing new modules
* Duplicate the [Google document with the example workflow](https://docs.google.com/document/d/1B-Q6VVFYGDCWbrDNRJtdsVoEtOTc-IXs/edit). Rename the file appropriately
* Use this file as a template to fill in information about your module
  * Do not change section headers
  * Sections that contain only bullet points are marked accordingly or other structured items are marked accordingly
  * Number of *activities* and *implementations* can be changed
* Add information about your module into [this table](https://docs.google.com/spreadsheets/d/1ex1oVwMyV4pyli-jmbz3H_dQE3uj83rRVdRw4l87lbc/edit?gid=0#gid=0)
* Notify the **SMWG group admins**. 
* Tasks for a group admin:
  * Create the files in the repo for the new module and move there the initial content.
  * Add link(s) to the master table [this table](https://docs.google.com/spreadsheets/d/1ex1oVwMyV4pyli-jmbz3H_dQE3uj83rRVdRw4l87lbc/edit?gid=0#gid=0)
  * Notify module developer
* Further editing can be done online (see Revising existing modules section above)

## Adding activities and implementations to the existing modules

**Activities** are exercises that illustrate concepts of the module. Each module must have at least one *activity*. *Activity* should be first described as a little protocol in the hardware-independent way. 
*Activity* needs to be written as a markdown file (free style), it can contain one or multiple figures.

Each *activity* must contain at least one **implementation**. Each *implementation* should contain step-by-step guidelines to run the protocol  described in the corresponding *activity*.

:::{note}
Everyone is welcome to contribute new activities and implementations. We are especially looking forward to industry partners adding implementations for their specific hardware and software.
:::

### Adding new activity
* Create a markdown file containing hardware agnostic activity description.
* Send a message to the SMWG group admins with a created markdown file and (optional) figures to be included.
* Tasks for a group admin:
  * Create the files in the repo for the new module and move there the initial content.
  * Notify module and activity developers
* Check the online version of the activity. Further editing can be done online (see *Revising existing modules section above*).

:::{note}
Remember to create at least one implementation for each new activity (see guidelines below).
:::

### Adding new implementation

* One of the following formats for implementations is possible.
  * A markdown file (.md)
  * A python script (.py)

* Create a file for new implementation.
* Send a message to the **SMWG group admins** with this file and information about the module and activity that it belongs to.
* Tasks for a group admin:
  * Move the new activity to GitHub Repository.
  * Notify module and activity developers.
* Check the online version of activity. Further editing can be done online (see Revising existing modules section above).


