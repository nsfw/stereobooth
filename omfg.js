
/*
 * Returns a list of the files in 'path' to the callback:
 * cb(error, ['file1', 'file2', ...])
 */
function apacheIndexList(path, cb) {
  $.ajax({
    url: path, 
    success: function(data) {
      /* Sanity check: is this an Apache directory index?
       */
      data = $('<html>').html(data);
      if($('title', data)[0].innerHTML.substr(0, 8) !==
        "Index of")
        return cb("Bad Apache directory index: " + path);
  
      /* Get all the hrefs after the "Parent Directory"
       * link: these are the contents of the directory.
       */
      var passedParentLink = false;
      var files = $('a', data).filter(function(i, a) {
        if(passedParentLink)
          return true;
        if(a.innerHTML.trim() === "Parent Directory")
           passedParentLink = true;
        return false;
      });
  
      var tidied = $(files).map(function(i, a) {
        if(a.href.substr(-1) === '/')
            return a.href.split('/').slice(-2,-1) + '/';
        return a.href.split('/').pop();
      });
  
      cb(null, tidied);
    },
    error: function(jqXHR, error, errorThrown) {
      cb(error);
    }
  });
}
