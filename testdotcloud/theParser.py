import re 
FILE = open("/home/murali/Desktop/2012-07-20_10:05:11_UTC.sql","r")
aaa = FILE.readlines()
FILE.close()
FILE = open("/home/murali/Desktop/server.sql","w")
display = 0
for aa in aaa:
	if re.search("TransactionsApp_users_groups",aa):
		break
	if re.search("INSERT INTO `TransactionsApp_users`",aa):
		aa = re.sub("\)",",NULL)",aa)
	if re.search("`lastPost_id` int",aa):
		FILE.write(aa)
		FILE.write("  `group_id` int(11) DEFAULT NULL,\n")
		FILE.write("  KEY `TransactionsApp_users_425ae3c4` (`group_id`),\n")
		FILE.write("  CONSTRAINT `group_id_refs_id_31e2d205` FOREIGN KEY (`group_id`) REFERENCES `TransactionsApp_groupstable` (`id`),\n")
	else:
		FILE.write(aa)
FILE.close()
			

