          if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")          

          if message.lower().lstrip().startswith(("-spa.", "!spam")):
            await self.highrise.chat("#NSS #NSS") 

          if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")  

          if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS")          

          if message.lower().lstrip().startswith(("-spam", "!spm")):
            await self.highrise.chat("#NSS #NSS") 

          if message.lower().lstrip().startswith(("-spam", "!spam")):
            await self.highrise.chat("#NSS #NSS") 


if message.lower().startswith("/getoutfit"):
  response = await self.highrise.get_my_outfit()
  for item in response.outfit:
      await self.highrise.chat(item.id)