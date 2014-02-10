StereoBooth
===========

RVIP Stereo Photobooth

This turns a couple (and maybe more) webcams in to a photo experience
that defies description! Which is totally going to save me time when
it comes to writing this Readme!

Requires:
* imagemagick (convert command) to convert from png to gif.
* scp is used to copy files to rvip.co, need to install the appropriate identity file to
  rvip.co.pem in the base directory where capture.py is run.
* Also requires cv2 and numpy python modules


Basic flow
==========

capture.py -
 captures the photo and stores it in local ./img directory

postFile -
 syncs the local ./img directory with the remote on rvip.co

on rvip.co --

omfg/index.html -- serves either the last NN images or a specific image passed in the URL
This is written jQuery Templates (which has been depricated), so may want to re-do in what ever the new hotness is.

https://github.com/BorisMoore/jquery-tmpl
http://stephenwalther.com/archive/2010/10/05/jquery-templates-on-microsoft-ajax-cdn


