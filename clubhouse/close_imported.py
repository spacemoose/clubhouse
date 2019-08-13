# Goal is to close issues that I already imported.


# First example: I used an external tool that saved the external id as
# https://.../GHI# Where GHI# is the issue number in github.  This
# external id doesn't exist in any other clubhouse isses, so all I
# have to do is search through all the clubhouse issues with a
# non-null external_id, check the last word (words seperated by /),
# and see if it matches the github number.
#
# If I find a match, I post a comment on the github issue saying
# "replaced by clubhouse#" and then I close the Github issue.
