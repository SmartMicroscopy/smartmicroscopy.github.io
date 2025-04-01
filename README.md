# Website of the Smart Microscopy Working Group

**Smart or Adaptive Feedback Microscopy** aims at connecting bioimage analysis (and other algorithms) with fully motorized and computer-controlled microscopes to generate automated and adaptive imaging workflows. This strategy can also be used to manage changes in the sample’s environment (e.g. fluidic devices) and directly link the microscope to image data management systems.

## Mission

While several software solutions for microscopy control exist and can be used to implement smart-microscopy workflows, there is no reference specification of what functionalities are needed, or how these workflows could be implemented. To facilitate the development of smart-microscopy applications, and enable their execution across imaging-systems with similar modalities, we are working to establish such a standard specification. 

The working group is composed of participants from both academia and industry, meeting regularly online with the support of the Euro-BioImaging Industry Board.

## Compiling the book locally
First you need a python installation.  
Then you need to install jupyter-book, either with `pip install -U jupyter-book` or `conda install -c conda-forge jupyter-book`.  
Clone this repository locally (or download the repo as a zip from github.com).  
In the repository root directory, open a command prompt (on windows, type `cmd` in the address bar).  
In the command prompt, type `./build_book.sh`, to run all the build scripts.

Note : If you get a message like *jupyter-book is not a recognized command*, make sure the directory containing the `jupyter-book.exe` is on your PATH. (On windows see environment variables).  

## Adding a profile
To add a new member profile, add the profile in `members/profiles/LastnameF.md`, then link the file in `members.md` & `_toc.yml`.
