from kickpy import *
from time import sleep
from datetime import datetime, timedelta
import time, string, asyncio, json, os, ast, re, sys, traceback
cl = LINE()
cl.log("Auth Token : " + str(cl.authToken))
cl.log("Mid : " + str(cl.getProfile().mid))
print("登入成功")
oepoll = OEPoll(cl)
clID = cl.getProfile().mid
Me = [clID, "ufe1707ae9b2ff7ab61505795b7995440"] #權限者
set = {
  "autoJoinKick": False,
  "autoJoinTicket": True
}
def bot(op):
     try:
         if op.type == 0:
            print("操作結束")
            return
         if op.type == 13:
           if set["autoJoinKick"] == True:
             cl.acceptGroupInvitation(op.param1)
             try:
                 G = cl.getGroup(op.param1)
                 targets = []
                 time.sleep(0.0001)
                 for member in G.members + G.invitee:
                      targets.append(member.mid)
                 for target in targets:
                     if target not in Me:
                       try:
    	                   cl.kickoutFromGroup(op.param1, [target])
                       except:
                           pass
                       try:
                           cl.cancelGroupInvitation(op.param1, [target])
                       except:
                           pass
             except:
             	pass
         if op.type == 25 or op.type == 26:
             msg = op.message
             text = str(msg.text)
             msg_id = msg.id
             receiver = msg.to
             sender = msg._from
             cmd = text.lower()
             time.sleep(0.0001)
             if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
               if sender != clID:
                 to = sender
               else:
                 to = receiver
             if msg.toType == 1:
               to = receiver
             if msg.toType == 2:
               to = receiver
             if msg.contentType == 0:
               if text is None:
                  return
               else:
                  if cmd == "*help":
                    if sender in Me:
                     cl.sendMessage(to, "*指令表*\n\n*kick@\n*kickall\n*cancelall\n*kickcancelall\n*status\n*about\n\n*設定*\najoinkick:on|off\njointicket:on|off")
                  if cmd =="*status":
                   if sender in Me:
                     stts = "Status"
                     if set["autoJoinKick"] == True: stts += "\n-AutoJoinKick:On"
                     else: stts += "\n-AutoJoinKick:Off"
                     if set["autoJoinTicket"] == True: stts += "\n-AutoJoinTicket:On"
                     else: stts += "\n-AutoJoinTicket:Off"
                     stts += ""
                     cl.sendMessage(to, str(stts))
                  if cmd =="joinkick:on":
                    if sender in Me:
                    	set["autoJoinKick"] = True
                    cl.sendMessage(to, "煙火開")
                  if cmd =="joinkick:off":
                    if sender in Me:
                    	set["autoJoinKick"] = False
                    cl.sendMessage(to, "煙火關")
                  if cmd =="ticket:on":
                    if sender in Me:
                    	set["autoJoinTicket"] = True
                    cl.sendMessage(to, "自動入群開")
                  if cmd =="ticket:off":
                    if sender in Me:
                    	set["autoJoinTicket"] = False
                    cl.sendMessage(to, "自動入群關")
                  if cmd =="*speed":
                    if sender in Me:
                     start = time.time()
                     time.sleep(0.0001)
                     elapsed_time = time.time() - start
                     cl.sendMessage(to, "{}".format(str(elapsed_time)))
                  if cmd =="*about":
                     cl.sendMessage(to, "Py翻機 v0.2\n\n作者: 尹莫")
                  if cmd =="*kickall":
                   if sender in Me:
                     G = cl.getGroup(to)
                     targets = []
                     time.sleep(0.0001)
                     for member in G.members:
                         targets.append(member.mid)
                     for target in targets:
                         if target not in Me:
                           try:
    	                       cl.kickoutFromGroup(to, [target])
                           except:
                              pass
                  if cmd == "*cancelall":
                   if sender in Me:
                     G = cl.getGroup(to)
                     targets = []
                     time.sleep(0.0001)
                     for member in G.invitee:
                         targets.append(member.mid)
                     for target in targets:
                         if target not in Me:
                           try:
    	                       cl.cancelGroupInvitation(to, [target])
                           except:
                              pass
                  if cmd =="*kickcancelall":
                    if sender in Me:
                     G = cl.getGroup(to)
                     targets = []
                     time.sleep(0.0001)
                     for member in G.members + G.invitee:
                         targets.append(member.mid)
                     for target in targets:
                         if target not in Me:
                           try:
    	                       cl.kickoutFromGroup(to, [target])
                           except:
                              pass
                           try:
                               cl.cancelGroupInvitation(to, [target])
                           except:
                              pass
                  if cmd.startswith("*kick "):
                    if sender in Me:
                      if 'MENTION' in msg.contentMetadata.keys()!= None:
                         names = re.findall(r'@(\w+)', text)
                         mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                         mentionees = mention['MENTIONEES']
                         targets = []
                         time.sleep(0.0001)
                         for mention in mentionees:
                             if mention["M"] not in targets:
                               targets.append(mention["M"])
                             for target in targets:
                             	if target not in Me:
                                   try:
                                        cl.kickoutFromGroup(to, [target])
                                   except:
                                        pass                                            
                  if "/ti/g/" in text.lower():
                    if set["autoJoinTicket"] == True:
                      link_re = re.compile("(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?")
                      links = link_re.findall(text)
                      n_links = []
                      for l in links:
                          if l not in n_links:
                            n_links.append(l)
                      for ticket_id in n_links:
                          findT = cl.findGroupByTicket(ticket_id)
                          if True:
                            cl.acceptGroupInvitationByTicket(findT.id, ticket_id)
     except Exception as e:
        cl.log("Error : " + str(e))
while True:
    try:
      ops=oepoll.singleTrace(count=50)
      if ops != None:
        for op in ops:
          bot(op)
          oepoll.setRevision(op.revision)
    except Exception as e:
        cl.log("Error : " + str(e))
