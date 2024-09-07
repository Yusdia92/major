from colorama import *
from datetime import datetime, timedelta
from fake_useragent import FakeUserAgent
from faker import Faker
import aiohttp
import asyncio
import json
import os
import sys

class Major:
    def __init__(self) -> None:
        self.faker = Faker()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Host': 'major.glados.app',
            'Pragma': 'no-cache',
            'Priority': 'u=1, i',
            'Referer': 'https://major.glados.app/?tgWebAppStartParam=6094625904',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': FakeUserAgent().random
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    async def tg_auth(self, queries: str):
        url = 'https://major.glados.app/api/auth/tg/'
        accounts = []
        async with aiohttp.ClientSession() as session:
            for query in queries:
                if not query:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Empty Query Found ]{Style.RESET_ALL}")
                    return
                data = json.dumps({'init_data':query})
                headers = {
                    **self.headers,
                    'Content-Length': str(len(data)),
                    'Content-Type': 'application/json',
                    'Origin': 'https://major.glados.app'
                }
                try:
                    async with session.post(url, headers=headers, data=data, timeout=20) as response:
                        response.raise_for_status()
                        tg_auth = await response.json()
                        token = f"Bearer {tg_auth['access_token']}"
                        id = tg_auth['user']['id']
                        first_name = tg_auth['user']['first_name'] or self.faker.first_name()
                        accounts.append({'first_name': first_name, 'id': id, 'token': token})
                except (aiohttp.ClientError, aiohttp.ContentTypeError, KeyError) as e:
                    self.print_timestamp(
                        f"{Fore.YELLOW + Style.BRIGHT}[ Failed To Process {query} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}"
                    )
        return accounts

    async def visit(self, token: str, first_name: str):
        url = 'https://major.glados.app/api/user-visits/visit/'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': '0',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    visit = await response.json()
                    if visit['is_increased']:
                        if visit['is_allowed']:
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.GREEN + Style.BRIGHT}[ Claimed Daily Visit ]{Style.RESET_ALL}"
                            )
                        else:
                            self.print_timestamp(
                                f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Subscribe Major Community To Claim Your Daily Visit Bonus And Increase Your Streak ]{Style.RESET_ALL}"
                            )
                    else:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Daily Visit Already Claimed ]{Style.RESET_ALL}"
                        )
            except aiohttp.ClientError:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Daily Visit: {str(e)} ]{Style.RESET_ALL}")
            except Exception:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Daily Visit: {str(e)} ]{Style.RESET_ALL}")

    async def streak(self, token: str, first_name: str):
        url = 'https://major.glados.app/api/user-visits/streak/'
        headers = {
            **self.headers,
            'Authorization': token
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching Streak: {str(e)} ]{Style.RESET_ALL}")
            except Exception:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching Streak: {str(e)} ]{Style.RESET_ALL}")

    async def user(self, token: str, id: str, first_name: str):
        url = f'https://major.glados.app/api/users/{id}/'
        headers = {
            **self.headers,
            'Authorization': token
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")

    async def squad(self, token: str, squad_id: int, first_name: str):
        url = f'https://major.glados.app/api/squads/{squad_id}'
        headers = {
            **self.headers,
            'Authorization': token
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    squad = await response.json()
                    self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Squad {squad['name']} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Squad Rating {squad['rating']} ]{Style.RESET_ALL}"
                    )
            except aiohttp.ClientError as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")

    async def join_squad(self, token: str, first_name: str):
        url = f'https://major.glados.app/api/squads/1904705154/join/'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': '0',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    join_squad = await response.json()
                    if join_squad['status'] == 'ok':
                        await self.squad(token=token, squad_id=1904705154, first_name=first_name)
            except aiohttp.ClientError as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")

    async def leave_squad(self, token: str, first_name: str):
        url = f'https://major.glados.app/api/squads/leave/'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': '0',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    leave_squad = await response.json()
                    if leave_squad['status'] == 'ok':
                        await self.join_squad(token=token, first_name=first_name)
            except aiohttp.ClientError as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching User: {str(e)} ]{Style.RESET_ALL}")

    async def tasks(self, token: str, type: str, first_name: str):
        url = f'https://major.glados.app/api/tasks/?is_daily={type}'
        headers = {
            **self.headers,
            'Authorization': token
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url=url, headers=headers, timeout=20) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Fetching Tasks: {str(e)} ]{Style.RESET_ALL}")

    async def complete_task(self, token: str, first_name: str, task_id: int, task_title: str, task_award: int):
        url = 'https://major.glados.app/api/tasks/'
        data = json.dumps({'task_id':task_id})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, data=data, timeout=20) as response:
                    response.raise_for_status()
                    complete_task = await response.json()
                    if complete_task['is_completed']:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ {task_title} Claimed, You've Got {task_award} ]{Style.RESET_ALL}"
                        )
            except aiohttp.ClientError as e:
                if e.status == 400:
                    return
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Complete {task_title}: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Complete {task_title}: {str(e)} ]{Style.RESET_ALL}")

    async def coins(self, token: str, first_name: str, reward_coins: int):
        url = 'https://major.glados.app/api/bonuses/coins/'
        data = json.dumps({'coins':reward_coins})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, data=data, timeout=20) as response:
                    if response.status == 400:
                        try:
                            error_coins = await response.json()
                            if 'detail' in error_coins:
                                if 'blocked_until' in error_coins['detail']:
                                    end_time = datetime.fromtimestamp(error_coins['detail']['blocked_until']).astimezone()
                                    formatted_end_time = end_time.strftime('%x %X %Z')
                                    return self.print_timestamp(
                                        f"{Fore.YELLOW + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT} | {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}[ Can Play Hold Coin At {formatted_end_time} ]{Style.RESET_ALL}"
                                    )
                        except aiohttp.ContentTypeError:
                            raise 'An HTTP 400 Error Occurred Without JSON Body While Play Hold Coin'
                    response.raise_for_status()
                    coins = await response.json()
                    if coins['success']:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ {first_name} Got {reward_coins} From Hold Coin ]{Style.RESET_ALL}"
                        )
            except aiohttp.ClientResponseError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Play Hold Coins: {str(e)} ]{Style.RESET_ALL}")
            except aiohttp.ClientError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} A Client Error Occurred While Play Hold Coins: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Play Hold Coins: {str(e)} ]{Style.RESET_ALL}")

    async def roulette(self, token: str, first_name: str):
        url = 'https://major.glados.app/api/roulette/'
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': '0',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, timeout=20) as response:
                    if response.status == 400:
                        try:
                            error_coins = await response.json()
                            if 'detail' in error_coins:
                                if 'blocked_until' in error_coins['detail']:
                                    end_time = datetime.fromtimestamp(error_coins['detail']['blocked_until']).astimezone()
                                    formatted_end_time = end_time.strftime('%x %X %Z')
                                    return self.print_timestamp(
                                        f"{Fore.YELLOW + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT} | {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}[ Can Play Roulette At {formatted_end_time} ]{Style.RESET_ALL}"
                                    )
                        except aiohttp.ContentTypeError:
                            raise 'An HTTP 400 Error Occurred Without JSON Body While Play Roulette'
                    response.raise_for_status()
                    roulette = await response.json()
                    self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Got {roulette['rating_award']} From Roulette ]{Style.RESET_ALL}"
                    )
            except aiohttp.ClientResponseError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")
            except aiohttp.ClientError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} A Client Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")

    async def swipe_coin(self, token: str, first_name: str, reward_swipe_coins: int):
        url = 'https://major.glados.app/api/swipe_coin/'
        data = json.dumps({'coins':reward_swipe_coins})
        headers = {
            **self.headers,
            'Authorization': token,
            'Content-Length': str(len(data)),
            'Content-Type': 'application/json',
            'Origin': 'https://major.glados.app'
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url=url, headers=headers, data=data, timeout=20) as response:
                    if response.status == 400:
                        try:
                            error_coins = await response.json()
                            if 'detail' in error_coins:
                                if 'blocked_until' in error_coins['detail']:
                                    end_time = datetime.fromtimestamp(error_coins['detail']['blocked_until']).astimezone()
                                    formatted_end_time = end_time.strftime('%x %X %Z')
                                    return self.print_timestamp(
                                        f"{Fore.YELLOW + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT} | {Style.RESET_ALL}"
                                        f"{Fore.YELLOW + Style.BRIGHT}[ Can Play Swipe Coin At {formatted_end_time} ]{Style.RESET_ALL}"
                                    )
                        except aiohttp.ContentTypeError:
                            raise 'An HTTP 400 Error Occurred Without JSON Body While Play Swipe Coin'
                    response.raise_for_status()
                    swipe_coin = await response.json()
                    if swipe_coin['success']:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {first_name} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT}[ Got {reward_swipe_coins} From Swipe Coin ]{Style.RESET_ALL}"
                        )
            except aiohttp.ClientResponseError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An HTTP Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")
            except aiohttp.ClientError as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} A Client Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")
            except Exception as e:
                return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {first_name} An Unexpected Error Occurred While Bonuses Coins: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        while True:
            try:
                queries = [line.strip() for line in open('queries.txt') if line.strip()]
                accounts = await self.tg_auth(queries=queries)
                total_rating = 0
                for account in accounts:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ {account['first_name']} Information ]{Style.RESET_ALL}")
                    await self.visit(token=account['token'], first_name=account['first_name'])
                    streak = await self.streak(token=account['token'], first_name=account['first_name'])
                    user = await self.user(token=account['token'], id=account['id'], first_name=account['first_name'])
                    self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {account['first_name']} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Balance {user['rating'] if user else 0} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.BLUE + Style.BRIGHT}[ Streak {streak['streak'] if streak else 0} ]{Style.RESET_ALL}"
                    )
                    if user['squad_id'] is None:
                        await self.join_squad(token=account['token'], first_name=account['first_name'])
                    elif user['squad_id'] != 1904705154:
                        await self.leave_squad(token=account['token'], first_name=account['first_name'])
                    else:
                        await self.squad(token=account['token'], first_name=account['first_name'], squad_id=user['squad_id'])
                for account in accounts:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ {account['first_name']} Tasks ]{Style.RESET_ALL}")
                    for type in ['true', 'false']:
                        tasks = await self.tasks(token=account['token'], type=type, first_name=account['first_name'])
                        for task in tasks:
                            if task['is_completed'] == False:
                                await self.complete_task(token=account['token'], first_name=account['first_name'], task_id=task['id'], task_title=task['title'], task_award=task['award'])
                                await asyncio.sleep(3)
                for account in accounts:
                    self.print_timestamp(f"{Fore.WHITE + Style.BRIGHT}[ {account['first_name']} Games ]{Style.RESET_ALL}")
                    await self.coins(token=account['token'], first_name=account['first_name'], reward_coins=915)
                    await self.roulette(token=account['token'], first_name=account['first_name'])
                    await self.swipe_coin(token=account['token'], first_name=account['first_name'], reward_swipe_coins=3200)

                    user = await self.user(token=account['token'], id=account['id'], first_name=account['first_name'])
                    if user:
                        total_rating += user['rating'] if user else 0

                self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ Total Account {len(accounts)} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.GREEN + Style.BRIGHT}[ Total Balance {total_rating} ]{Style.RESET_ALL}"
                )

                sleep_timestamp = datetime.now().astimezone() + timedelta(seconds=1800)
                timestamp_sleep_time = sleep_timestamp.strftime('%X %Z')
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ Restarting At {timestamp_sleep_time} ]{Style.RESET_ALL}")
                await asyncio.sleep(1800)
                self.clear_terminal()
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
                continue

if __name__ == '__main__':
    try:
        init(autoreset=True)
        major = Major()
        asyncio.run(major.main())
    except (Exception, aiohttp.ClientError, json.JSONDecodeError) as e:
        major.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)
