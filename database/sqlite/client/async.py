import asyncio
import aiosqlite
from typing import NoReturn
import timeit


DB = "../slow.db"
COLORS = [
    "\033[95m",
    "\033[94m",
    "\033[96m",
    "\033[92m",
    "\033[93m"
]
ENDC = "\033[0m"

SLOW_QUERY = """
    SELECT c.name, s.state FROM cities c
    JOIN states s ON  c.state_id = s.id
    WHERE s.state IN (
        SELECT state FROM states
    )
    ORDER BY s.long_name, c.name
"""
MEDIUM_QUERY = """
    SELECT c.name, s.state FROM cities c
    JOIN states s ON  c.state_id = s.id
    WHERE s.state like 'M%' OR s.state like '%P'
"""
FAST_QUERY = """
    SELECT c.name, s.state FROM cities c
    JOIN states s ON  c.state_id = s.id
    WHERE c.name like '%A'
"""


class Requester:
    rid: int = 0

    def __init__(self):
        Requester.rid += 1
        self.rid = Requester.rid
        self.color = COLORS[self.rid]

    async def query_from_db(self, query: str) -> NoReturn:
        prefix = f"{self.color}R{self.rid}: "
        suffix = f"{ENDC}"
        print(f"{prefix}Querying '{query}'{suffix}")

        async with aiosqlite.connect(DB) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute(query) as cursor:
                rows = await cursor.fetchall()
                content = len(rows)

        print(f"{prefix}Query made! Db replied '{content}' rows{suffix}")


async def main():
    r1 = Requester()
    r2 = Requester()
    r3 = Requester()

    print("=" * 10)
    starttime = timeit.default_timer()

    await asyncio.gather(
        r1.query_from_db(SLOW_QUERY),
        r2.query_from_db(FAST_QUERY),
        r3.query_from_db(MEDIUM_QUERY)
    )

    print("-" * 10)
    print(f"Time elapsed: {timeit.default_timer() - starttime}")
    print("=" * 10)

if __name__ == "__main__":
    asyncio.run(main())
