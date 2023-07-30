import aiomysql
import asyncio

class Database:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.pool = None
    
    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            port=self.port,
            autocommit=True,
            loop=asyncio.get_event_loop(),
            minsize=5,
            maxsize=10
        )
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SET SESSION wait_timeout = 864000")
        print("DB Pool started")
    async def close(self):
        self.pool.close()
        await self.pool.wait_closed()
    
    async def insert_user_balance(self, user_id, wallet, bank):
        query = "INSERT INTO economy_balance (user_id, wallet, bank) VALUES (%s, %s, %s) " \
                "ON DUPLICATE KEY UPDATE wallet = VALUES(wallet), bank = VALUES(bank)"
        await self.execute(query, user_id, wallet, bank)

    async def get_user_balance(self, user_id):
        query_select = "SELECT wallet, bank FROM economy_balance WHERE user_id = %s"
        query_insert = "INSERT INTO economy_balance (user_id, wallet, bank) VALUES (%s, %s, %s)"

        # Check if the user exists in the database
        result = await self.execute(query_select, user_id)

        if result:
            # User exists, return both wallet and bank balances
            return result[0][0], result[0][1]
        else:
            # User doesn't exist, create a new row with default wallet and bank balances
            default_wallet = 0
            default_bank = 0
            await self.execute(query_insert, user_id, default_wallet, default_bank)
            return default_wallet, default_bank

    async def get_wallet_balance(self, user_id):
        query_select = "SELECT wallet FROM economy_balance WHERE user_id = %s"
        query_insert = "INSERT INTO economy_balance (user_id, wallet, bank) VALUES (%s, %s, %s)"

        result = await self.execute(query_select, user_id)

        if result:
            return result[0][0]  # Return the wallet balance if the user exists
        else:
            default_wallet = 0
            default_bank = 0

            await self.execute(query_insert, user_id, default_wallet, default_bank)

            return default_wallet
    
    async def transfer_wallet_to_bank(self, user_id, amount):
        # Get the current wallet and bank balance of the user
        query_select = "SELECT wallet, bank FROM economy_balance WHERE user_id = %s"
        user_data = await self.execute(query_select, user_id)

        if not user_data:
            return False  # User not found in the table

        current_wallet = user_data[0][0]
        current_bank = user_data[0][1]

        # Check if the user has enough balance in the wallet
        if current_wallet >= amount:
            # Perform the transfer
            query_update = "UPDATE economy_balance SET wallet = wallet - %s, bank = bank + %s WHERE user_id = %s"
            await self.execute(query_update, amount, amount, user_id)
            return True
        else:
            return False  # Insufficient balance in the wallet

    async def transfer_bank_to_wallet(self, user_id, amount):
        # Get the current wallet and bank balance of the user
        query_select = "SELECT wallet, bank FROM economy_balance WHERE user_id = %s"
        user_data = await self.execute(query_select, user_id)

        if not user_data:
            return False  # User not found in the table

        current_wallet = user_data[0][0]
        current_bank = user_data[0][1]

        # Check if the user has enough balance in the bank
        if current_bank >= amount:
            # Perform the transfer
            query_update = "UPDATE economy_balance SET wallet = wallet + %s, bank = bank - %s WHERE user_id = %s"
            await self.execute(query_update, amount, amount, user_id)
            return True
        else:
            return False  # Insufficient balance in the bank
        
    async def add_to_wallet(self, user_id, amount):
        query_update = "UPDATE economy_balance SET wallet = wallet + %s WHERE user_id = %s"
        await self.execute(query_update, amount, user_id)

    async def add_to_bank(self, user_id, amount):
        query_update = "UPDATE economy_balance SET bank = bank + %s WHERE user_id = %s"
        await self.execute(query_update, amount, user_id)

    async def execute(self, query, *args):
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
                    return await cur.fetchall()
        except aiomysql.exceptions.OperationalError:
            # Reconnect in case of a connection issue
            print("Lost connection, reconnecting...")
            await self.connect()
            # Retry the execution of the query
            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, args)
                    return await cur.fetchall()