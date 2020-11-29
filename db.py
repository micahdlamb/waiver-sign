import os
import aioodbc

async def connect():
    global pool
    pool = await aioodbc.create_pool(dsn=f"""
        DRIVER={os.environ['db_driver']};
        SERVER=medfairprice.database.windows.net;
        DATABASE=medfairprice;
        UID={os.environ['db_uid']};
        PWD={os.environ['db_pwd']};
    """)

def acquire_cursor(func):
    async def wrap(*args, **kwds):
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                return await func(cur, *args, **kwds)
    return wrap

@acquire_cursor
async def save_waiver(cur, template_id, bytes, fields):
    await cur.execute("""
        insert into waiver(waiver_template_id, pdf_bytes)
        values(?, ?)
    """, template_id, bytes)
    await cur.execute("SELECT @@IDENTITY")
    row = await cur.fetchone()
    waiver_id = row[0]
    for name, value in fields.items():
        await cur.execute("""
            insert into waiver_field(waiver_id, name, value)
            values(?, ?, ?)
        """, waiver_id, name, value)
    await cur.commit()

@acquire_cursor
async def get_waivers(cur, template_id):
    await cur.execute("""
        select waiver_id, create_date
        from waiver
        where waiver_template_id = ?
        order by create_date desc
    """, template_id)
    waivers = [dict(id=row[0], create_date=row[1].timestamp()) for row in await cur.fetchall()]
    for waiver in waivers:
        await cur.execute("""
            select name, value
            from waiver_field
            where waiver_id = ?
        """, waiver['id'])
        waiver['values'] = {row[0] : row[1] for row in await cur.fetchall()}
    return waivers

@acquire_cursor
async def get_pdf(cur, template_id, id):
    await cur.execute("""
        select pdf_bytes from waiver where waiver_template_id = ? and waiver_id = ?
    """, template_id, id)
    row = await cur.fetchone()
    return row[0]