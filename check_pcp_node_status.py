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
      "usage: %s -H host -P port -u user -p pass [-n node]" % sys.argv[0])

def nagios_return(code, response):
  """ prints the response message
      and exits the script with one
      of the defined exit codes
      DOES NOT RETURN
  """
  print code + ": " + response
  sys.exit(nagios_codes[code])

def do_nodeinfo_check(host, port, user, pwd, node):
  retcode=0
  args = ["pcp_node_info", "30", host, port, user, pwd, node]
  try:
      p = subprocess.Popen(args, stdout=subprocess.PIPE)
  except OSError:
    retcode=-1
    s = 0
    w = 0
  if (retcode!=-1):
    p.wait()
    retcode = p.returncode
    out = p.communicate()[0].strip()
    ov = out.split()
    s = ov[2]
    w = ov[3]
  return [retcode, s, w]

def get_node_count(host, port, user, pwd):
  retcode=0
  args = ["pcp_node_count", "30", host, port, user, pwd]
  try:
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
  except OSError:
    retcode=-1
    c=0
  if (retcode!=-1):
    p.wait()
    retcode = p.returncode
    out = p.communicate()[0].strip()
    c=int(out)
  return [retcode,c]


def check_condition(host, port, user, pwd, node):
  ret={}
  if (node!=None):
    (retcode, status, weight) = do_nodeinfo_check(host, port, user, pwd, node)
    if (retcode!=0):
      ret={"code": "UNKNOWN", "message": "pcp_node_info returned non zero"}
    else:
      if (status == '2'):
        ret={"code": "OK", "message": "Node Status OK - Weight %s" % weight}
      elif (status == '3'):
        ret={"code": "CRITICAL", "message": "Node Status CRITICAL - Node down"}
      else:
        ret={"code": "UNKNOWN", "message": "Node Status Unknown - %s" % status}
  else:
    upnodes=[]
    downnodes=[]
    (r,count)=get_node_count(host, port, user, pwd)
    if (r==-1):
      ret={"code": "UNKNOWN", "message": "Error running pcp_node_count"}
    for i in range(count):
      (retcode, status, weight) = do_nodeinfo_check(host, port, user, pwd, str(i))
      if (retcode!=0):
        ret={"code": "UNKNOWN", "message": "pcp_node_info returned non zero"}
        break
      if (status=='2'):
        upnodes.append([i,status])
      else:
        downnodes.append([i,status])

    if (ret.has_key("code")):
      return ret  # Ug I hate returning in more than 1 place in a function

    if (len(downnodes)==0):
      ret={"code": "OK", "message": "%d nodes up" % count}
    else:
      m = ""
      for n in downnodes:
        m = m + "Node: %s, Status: %s " % (n[0], n[1])
      ret={"code": "CRITICAL", "message": m}
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
  if (host == None or port == None or user == None or pwd == None):
    usage()

  result = check_condition(host, port, user, pwd, node)
  nagios_return(result['code'], result['message'])

if __name__ == "__main__":
  main()
