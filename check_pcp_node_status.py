#!/usr/bin/env python
# check_pcp_node_status - check PGPool node status
#
# Python Nagios Template from
# http://bsd.dischaos.com/2009/04/29/nagios-plugin-template-in-python/

import sys, getopt, subprocess

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
  args = ["pcp_node_info", "30", host, port, user, pwd, node]
  try:
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
  except OSError:
    retcode=-1
  p.wait()
  retcode = p.returncode
  out = p.communicate()[0]
  out.strip()
  ov = out.split()
  if (retcode!=0):
    ret={"code": "UNKNOWN", "message": "pcp_node_info returned non zero"}
  else:
    if (ov[2] == '2'):
      ret={"code": "OK", "message": "Node Status OK - Weight %s" % ov[3]}
    elif (ov[2] == '3'):
      ret={"code": "CRITICAL", "message": "Node Status CRITICAL - Node down"}
    else:
      ret={"code": "UNKNOWN", "message": "Node Status Unknown - %s" % ov[2]}
  return ret

def main():
  host=None
  port=None
  user=None
  pwd=None
  node=None

  if len(sys.argv) < 2:
    usage()

  try:
    opts, args = getopt.getopt(sys.argv[1:], "H:P:u:p:n:")
  except getopt.GetoptError, err:
    usage()

  for o, value in opts:
    if (o == "-H"):
      host = value
    elif (o == "-P"):
      port = value
    elif (o == "-u"):
      user = value
    elif (o == "-p"):
      pwd = value
    elif (o == "-n"):
      node = value
    else:
      usage()
  if (host == None or port == None or user == None or pwd == None or node == None):
    usage()

  result = check_condition(host, port, user, pwd, node)
  nagios_return(result['code'], result['message'])

if __name__ == "__main__":
  main()
