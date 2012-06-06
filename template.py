#!/usr/bin/env python

# Adapted from Python Nagios Template from
# http://bsd.dischaos.com/2009/04/29/nagios-plugin-template-in-python/

import sys, getopt

nagios_codes = {'OK': 0,
    'WARNING': 1,
    'CRITICAL': 2,
    'UNKNOWN': 3,
    'DEPENDENT': 4}

def usage():
  """ returns nagios status UNKNOWN with
        a one line usage description
        usage() calls nagios_return()
  """
  nagios_return('UNKNOWN',
      "usage: %s -H host -P port -u user -p pass -n node" % sys.argv[0])

def nagios_return(code, response):
  """ prints the response message
      and exits the script with one
      of the defined exit codes
      DOES NOT RETURN
  """
  print code + ": " + response
  sys.exit(nagios_codes[code])

def check_condition(host, port, user, pwd, node):
  ret={"code": "UNKNOWN", "message": "NO CHECK CONDITION DEFINED"}
  return ret

def main():
  host=None

  if len(sys.argv) < 2:
    usage()

  try:
    opts, args = getopt.getopt(sys.argv[1:], "H:P:u:p:n:")
  except getopt.GetoptError, err:
    usage()

  for o, value in opts:
    if (o == "-H"):
      host = value
  if (host == None):
    usage()

  result = check_condition(host, port, user, pwd, node)
  nagios_return(result['code'], result['message'])

if __name__ == "__main__":
  main()
