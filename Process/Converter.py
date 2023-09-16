# -*- coding: utf-8 -*-
'''
Created on 16 sept. 2023

@author: BoxBoxJason
'''

import re
from datetime import datetime
def convertTxtToJson(messagesLines):

    jsonMsg = {"participants":set(),"messages":[]}
    for line in messagesLines:

        if re.match('^\d{2}\/\d{2}\/\d{4}$',line[:10]):
            msgDateTime = datetime(int(line[6:10]),int(line[3:5]),int(line[:2]),int(line[12:14]),int(line[15:17]))

            msgStart = line.find(":",20)
            if msgStart != -1:
                user = line[20:msgStart]
                message = line[msgStart+2:]

                jsonMsg["participants"].add(user)
                jsonMsg["messages"].append({"datetime":msgDateTime,"user":user,"message":message})
        else:
            jsonMsg["messages"][-1]["message"] += f"\n{line}"

    return jsonMsg
