import logging

from core.base import async_session

logging.info(f"async_session imported: {async_session}")

def connection(func):
    async def inner(*args, **kwargs):
        logging.info(f"🔧 [conn.py] About to open session from: {async_session}")
        session_obj = async_session()
        logging.info(
            "🧪 [conn.py] session_obj = async_session(): %s (type: %s)",
            session_obj,
            type(session_obj),
        )

        try:
            async with session_obj as session:
                logging.info("✅ [conn.py] Successfully opened session")
                result = await func(session, *args, **kwargs)
                logging.info("🔁 [conn.py] Function executed with DB session")
                return result
        except Exception as e:
            logging.info(f"❌ [conn.py] Exception inside connection wrapper: {e}")
            raise e
    return inner
