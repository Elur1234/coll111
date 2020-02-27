import discord
import config
from discord import utils
from discord.ext import commands
import random
class MyClient(discord.Client):
    
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):   
        if payload.message_id == config.POST_ID:
            role = None
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
            try:
                if (config.rol1 == 0):
                    role = utils.get(message.guild.roles, id=config.ROLES['1']) # объект выбранной роли (если есть)
                    config.rol1 = 1
                    config.rol1_user = member
                    
                elif (config.rol2 == 0):
                    role = utils.get(message.guild.roles, id=config.ROLES['2']) # объект выбранной роли (если есть)
                    config.rol2 = 1
                    config.rol2_user = member
                    
                elif (config.rol3 == 0):
                    role = utils.get(message.guild.roles, id=config.ROLES['3']) # объект выбранной роли (если есть)
                    config.rol3 = 1
                    config.rol3_user = member
                else:
                    config.rol_ojid.append(member)
                    role = utils.get(message.guild.roles, id=config.ROLES['4'])
           
                if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))
           
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
    
    async def on_raw_reaction_remove(self, payload):
        role = None
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
 
        try:
            l = 0
            for e in config.rol_ojid:
                if (e == member):
                    pop = 1
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            gog = None
            j = 1
            if (config.rol1_user == member):
                for e in config.rol_ojid:
                    gog = e
                    await gog.remove_roles(utils.get(message.guild.roles, id=config.ROLES['4']))
                    await gog.add_roles(utils.get(message.guild.roles, id=config.ROLES['1']))
                    if (gog != ''):
                        j = 0
                        config.rol_ojid.remove(gog)
                        config.rol1 = 1
                        config.rol1_user = gog
                    break
                if (j == 1):
                    config.rol1 = 0
                    config.rol1_user = ''
                role = utils.get(message.guild.roles, id=config.ROLES['1'])
            elif (config.rol2_user == member):
                for e in config.rol_ojid:
                    gog = e
                    await gog.remove_roles(utils.get(message.guild.roles, id=config.ROLES['4']))
                    await gog.add_roles(utils.get(message.guild.roles, id=config.ROLES['2']))
                    if (gog != ''):
                        j = 0
                        config.rol_ojid.remove(gog)
                        config.rol2 = 1
                        config.rol2_user = gog
                    break
                if (j == 1):
                    config.rol2 = 0
                    config.rol2_user = ''
                role = utils.get(message.guild.roles, id=config.ROLES['2'])
            elif (config.rol3_user == member):
                for e in config.rol_ojid:
                    gog = e
                    await gog.remove_roles(utils.get(message.guild.roles, id=config.ROLES['4']))
                    await gog.add_roles(utils.get(message.guild.roles, id=config.ROLES['3']))
                    if (gog != ''):
                        j = 0
                        config.rol_ojid.remove(gog)
                        config.rol3 = 1
                        config.rol3_user = gog
                    break
                if (j == 1):
                    config.rol3 = 0
                    config.rol3_user = ''
                role = utils.get(message.guild.roles, id=config.ROLES['3'])
            elif (pop == 1):
                config.rol_ojid.remove(member)
                role = utils.get(message.guild.roles, id=config.ROLES['4'])
                
            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
    
    admin = []
    async def on_message(self, message):
        mes = '{0.content}'.format(message)
        nic = '{0.author}'.format(message)
        if (mes == '!play'):
            f = open('name.txt', 'r')
            i = 0
            y = 0
            for e in f:
                i = i + 1
                if (e == nic + '\n'):
                    y = 1
                    break
            f.close()
            if (y == 1):
               f = open('bal.txt', 'r')
               q = 0
               pal = 0
               n = ''
               for e in f:
                    e = int(e)
                    q = q + 1
                    if(q == i):
                        e = e - 10
                        if (e == -10):
                            e = e + 10
                            await message.channel.send(nic + ', на вашем балансе 0, вы не можете крутить барабан \nОбратитесь к модератором за пополнением баланса')
                            n = n + str(e) + '\n'
                            continue
                        pal = e
                        await message.channel.send(nic + ', баланс до кручения: ' + str(pal + 10))
                        await message.channel.send('Начинаем крутить барабан')
                        ran = random.randint(0, 999)
                        print(ran)
                        if (ran > config.B_ and ran < config.C_):
                            pal = pal + 50
                            await message.channel.send('Ты забрал приз, твой баланс: ' + str(pal))
                        elif (ran > config.C_):
                            pal = pal + 500
                            await message.channel.send('Ты забрал супер приз, твой баланс: ' + str(pal))
                        else:
                            await message.channel.send('Ты проиграл, твой баланс: ' + str(pal))
                        e = pal
               f.close()
               q = 0
               f = open('bal.txt', 'r')
               for e in f:
                   e = int(e)
                   q = q + 1
                   if (q == i):
                       e = pal
                   n = n + str(e) + '\n'
               f.close()
               f = open('bal.txt', 'w')
               f.write(n)
               f.close()
            else:
                f = open('name.txt', 'a')
                f.write(nic + '\n')
                f.close()
                f = open('bal.txt', 'a')
                f.write('1000\n')
                f.close()
                await message.channel.send('Мы незнаем кто вы, но мы вас зарегистрировали под ником {0.author} и у вас на счету 1000 баллов'.format(message))
        elif (mes == '!cash'):
            f = open('name.txt', 'r')
            mes = '{0.content}'.format(message)
            nic = '{0.author}'.format(message)
            g = 0
            i = 0
            y = 0
            e = None
            for e in f:
                i = i + 1
                if (e == nic + '\n'):
                    y = 1
                    break
            f.close()
            f = open('bal.txt', 'r')
            for e in f:
                g = g + 1
                if (g == i):
                    await message.channel.send('Твой баланс: ' + str(e))
        elif (mes == '!ret'):
            config.rol1 = 0
            config.rol3 = 0
            config.rol2 = 0
            config.rol1_user = ''
            config.rol3_user = ''
            config.rol2_user = ''
            print('Done')
        elif (mes == '!del1'):
            config.rol1 = 0
            config.rol1_user = ''
        elif (mes == '!del2'):
            config.rol2 = 0
            config.rol2_user = ''
        elif (mes == 'del3'):
            config.rol3 = 0
            config.rol3_user = ''

client = MyClient()
client.run('Njc3NDU4MTA4MjQ2NjU0OTg2.XkU75Q.Eua0bjlppidNMgLUK6Gmc9lrt_o')
