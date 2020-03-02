# jiraclient
Small class to interact with a Jira server

# Synopsis
We had a problem with Jira versions. When creating new workflows in projects we never bothered to set the archive attribute to `true`. When we finally upgraded from version 6 to version 7, boards blew up because they were fetching all unarchived versions and timing out when trying to paginate and display them in the web interface.
Quick search showed that there was no suitable "bulk archiver" to set the attribute on multiple files so I had to write this myself as a way to fix the problem, remove some rust with writing python code and make sure that it can be extended to do other stuff vs. Jira as well.
