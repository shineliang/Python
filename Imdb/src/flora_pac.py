#!/usr/bin/env python
#
# Flora_Pac by @leaskh
# www.leaskh.com, i@leaskh.com
#
# based on chnroutes project (by Numb.Majority@gmail.com)
#

import re
import urllib2
import argparse
import math


def generate_pac(proxy):
    results  = fetch_ip_data()
    pacfile  = 'flora_pac.pac'
    rfile    = open(pacfile, 'w')
    strLines = """
// Flora_Pac by @leaskh
// www.leaskh.com, i@leaskh.com

function FindAgsProxyForURL(url, host) {
    return "PROXY 119.119.119.9:8080";
}

function FindGoagentProxyForURL(url, host) {
    return "%s";
}

function FindProxyForURL(url, host)
{
	if (isInNet(host, "119.119.0.0", "255.255.0.0")
		|| isInNet(host, "10.0.0.0", "255.0.0.0")
		|| shExpMatch(host, "64.75.47.10")
		|| shExpMatch(url, "*mail.amaxgs.com/*")) {
			return "DIRECT";
	} else if (shExpMatch(url, "*.google.com/*")) {
			return FindGoagentProxyForURL(url, host);
	}

    var list = [
""" % (proxy)

    intLines = 0
    for ip,mask,_ in results:
        if intLines > 0:
            strLines = strLines + ','
        intLines = intLines + 1
        strLines = strLines + "\n        ['%s', '%s']"%(ip, mask)    
    strLines = strLines + (
        "\n    ];"
        "\n"
        "\n    var ip = dnsResolve(host);"
        "\n"
        "\n    for (var i in list) {"
        "\n        if (isInNet(ip, list[i][0], list[i][1])) {"
        "\n            return FindAgsProxyForURL(url, host);"
        "\n        }"
        "\n    }"
        "\n"
        "\n    return FindGoagentProxyForURL(url, host);"
        "\n"
        "\n}"
        "\n"
    )
    rfile.write(strLines)
    rfile.close()
    print ("Rules: %d items.\n"
           "Usage: Use the newly created %s as your web browser's automatic "
           "proxy configuration (.pac) file."%(intLines, pacfile))


def fetch_ip_data():
    #fetch data from apnic
    print "Fetching data from apnic.net, it might take a few minutes, please wait..."
    url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    data=urllib2.urlopen(url).read()

    cnregex=re.compile(r'apnic\|cn\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    cndata=cnregex.findall(data)

    results=[]

    for item in cndata:
        unit_items=item.split('|')
        starting_ip=unit_items[3]
        num_ip=int(unit_items[4])

        imask=0xffffffff^(num_ip-1)
        #convert to string
        imask=hex(imask)[2:]
        mask=[0]*4
        mask[0]=imask[0:2]
        mask[1]=imask[2:4]
        mask[2]=imask[4:6]
        mask[3]=imask[6:8]

        #convert str to int
        mask=[ int(i,16 ) for i in mask]
        mask="%d.%d.%d.%d"%tuple(mask)

        #mask in *nix format
        mask2=32-int(math.log(num_ip,2))

        results.append((starting_ip,mask,mask2))

    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description="Generate proxy auto-config rules.")
    parser.add_argument('-x', '--proxy',
                        dest = 'proxy',
                        default = 'PROXY 127.0.0.1:8087',
                        nargs = '?',
                        help = "Proxy Server, examples: "
                               "SOCKS 127.0.0.1:8964; "
                               "SOCKS5 127.0.0.1:8964; "
                               "PROXY 127.0.0.1:8964")

    args = parser.parse_args()

    generate_pac(args.proxy)
