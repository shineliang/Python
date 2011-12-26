'''
Created on Dec 26, 2011

@author: shine_zhong
'''

if __name__ == '__main__':
    print "test"
    str = 'Anjan Garai <Anjan.Garai@bhnetwork.com>; Anoop Balakrishnan <Anoop.Balakrishnan@safeway.com>; Bhavini Patel <Bhavini.Patel@bhnetwork.com>; Biju Nair <Biju.Balakrishnan2@bhnetwork.com>; Cherian Mathew <Cherian.Mathew@bhnetwork.com>; Hari Cheruku <Hari.Cheruku@bhnetwork.com>; Lawrence Fernandes <Lawrence.Fernandes@bhnetwork.com>; Len Chao <Len.Chao@bhnetwork.com>; Lloyd Fernandes <Lloyd.Fernandes@bhnetwork.com>; Manish Kr <Manish.Kr@bhnetwork.com>; Rohit Sharma <Rohit.Sharma@bhnetwork.com>; Swarnalatha Kothakota <Swarnalatha.Kothakota@bhnetwork.com>; Vinay Purwar <Vinay.Purwar@bhnetwork.com>; shine_zhong@amaxgs.com; Bruce Li <bruce_li@amaxgs.com>; echo_wang@amaxgs.com'
    list = str.split('; ')
    for item in list:
        names = item.split(' <')
        print names[0]
    